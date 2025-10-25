from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from typing import Dict, Set
import asyncio
import logging
import json

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.models.camera import Camera
from app.models.detection import Detection
from app.services.camera_service import camera_service
from app.models.alert import Alert, AlertSeverity
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter()


class ConnectionManager:
    """Manage WebSocket connections"""

    def __init__(self):
        # user_id -> set of websockets
        self.active_connections: Dict[int, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        """Accept and register a new connection"""
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)
        logger.info(f"User {user_id} connected via WebSocket")

    def disconnect(self, websocket: WebSocket, user_id: int):
        """Remove a connection"""
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        logger.info(f"User {user_id} disconnected from WebSocket")

    async def send_to_user(self, user_id: int, message: dict):
        """Send message to all connections of a user"""
        if user_id in self.active_connections:
            disconnected = set()
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending message: {e}")
                    disconnected.add(connection)

            # Remove disconnected connections
            for conn in disconnected:
                self.disconnect(conn, user_id)

    async def broadcast_to_user(self, user_id: int, message: str):
        """Broadcast text message to user"""
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_text(message)
                except Exception:
                    pass


manager = ConnectionManager()


async def get_user_from_token(token: str, db: Session) -> User:
    """Get user from JWT token"""
    payload = decode_access_token(token)
    if not payload:
        return None

    user_id = payload.get("sub")
    if not user_id:
        return None

    user = db.query(User).filter(User.id == int(user_id)).first()
    return user


@router.websocket("/stream/{camera_id}")
async def websocket_camera_stream(
    websocket: WebSocket,
    camera_id: int,
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    """
    WebSocket endpoint for real-time camera streaming
    """
    # Authenticate user
    user = await get_user_from_token(token, db)
    if not user:
        await websocket.close(code=1008, reason="Authentication failed")
        return

    # Verify camera ownership
    camera = db.query(Camera).filter(
        Camera.id == camera_id,
        Camera.owner_id == user.id
    ).first()

    if not camera:
        await websocket.close(code=1008, reason="Camera not found")
        return

    await manager.connect(websocket, user.id)

    try:
        # Start camera if not active
        if camera_id not in camera_service.active_streams:
            success = camera_service.open_camera(
                camera_id,
                camera.source,
                camera.source_type
            )
            if not success:
                await websocket.send_json({
                    "type": "error",
                    "message": "Failed to start camera stream"
                })
                return

        # Stream frames
        async for frame_data in camera_service.stream_frames(
            camera_id,
            camera.detection_enabled,
            camera.confidence_threshold,
            camera.fps
        ):
            # Send frame to client
            await websocket.send_json({
                "type": "frame",
                "data": frame_data
            })

            # If suspicious activity detected, create detection and alert
            if frame_data.get("has_suspicious_activity") and frame_data.get("detections"):
                for detection_data in frame_data["detections"]:
                    # Create detection record
                    detection = Detection(
                        camera_id=camera_id,
                        detection_type=detection_data.get("detection_type", "person_detected"),
                        confidence=detection_data["confidence"],
                        bbox_x1=detection_data["bbox"]["x1"],
                        bbox_y1=detection_data["bbox"]["y1"],
                        bbox_x2=detection_data["bbox"]["x2"],
                        bbox_y2=detection_data["bbox"]["y2"],
                        extra_data=detection_data
                    )
                    db.add(detection)
                    db.flush()

                    # Create alert
                    alert = Alert(
                        detection_id=detection.id,
                        user_id=user.id,
                        title="Suspicious Activity Detected",
                        message=f"Suspicious activity detected on camera {camera.name}",
                        severity=AlertSeverity.HIGH
                    )
                    db.add(alert)

                    # Update camera last detection
                    camera.last_detection = datetime.utcnow()

                db.commit()

                # Send alert notification
                await websocket.send_json({
                    "type": "alert",
                    "message": "Suspicious activity detected!",
                    "camera_id": camera_id,
                    "camera_name": camera.name
                })

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for camera {camera_id}")
    except Exception as e:
        logger.error(f"Error in WebSocket stream: {e}")
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })
    finally:
        manager.disconnect(websocket, user.id)


@router.websocket("/notifications")
async def websocket_notifications(
    websocket: WebSocket,
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    """
    WebSocket endpoint for real-time notifications
    """
    # Authenticate user
    user = await get_user_from_token(token, db)
    if not user:
        await websocket.close(code=1008, reason="Authentication failed")
        return

    await manager.connect(websocket, user.id)

    try:
        # Send welcome message
        await websocket.send_json({
            "type": "connected",
            "message": "Connected to notification stream"
        })

        # Keep connection alive and listen for messages
        while True:
            try:
                # Receive messages from client (heartbeat, etc.)
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)

                # Echo back (heartbeat response)
                await websocket.send_json({
                    "type": "pong",
                    "timestamp": datetime.utcnow().isoformat()
                })

            except asyncio.TimeoutError:
                # Send heartbeat
                await websocket.send_json({
                    "type": "heartbeat",
                    "timestamp": datetime.utcnow().isoformat()
                })

    except WebSocketDisconnect:
        logger.info(f"Notification WebSocket disconnected for user {user.id}")
    except Exception as e:
        logger.error(f"Error in notification WebSocket: {e}")
    finally:
        manager.disconnect(websocket, user.id)


# Export manager for use in other modules
__all__ = ["router", "manager"]
