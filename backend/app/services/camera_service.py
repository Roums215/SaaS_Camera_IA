import cv2
import numpy as np
import asyncio
import logging
from typing import Optional, Dict, AsyncGenerator
import base64
from datetime import datetime

from app.services.detection_service import detection_service

logger = logging.getLogger(__name__)


class CameraStreamService:
    """Service for managing camera streams"""

    def __init__(self):
        self.active_streams: Dict[int, cv2.VideoCapture] = {}
        self.stream_tasks: Dict[int, asyncio.Task] = {}

    def open_camera(self, camera_id: int, source: str, source_type: str = "webcam") -> bool:
        """
        Open camera stream
        """
        try:
            if camera_id in self.active_streams:
                self.close_camera(camera_id)

            # Determine source
            if source_type == "webcam":
                # Convert source to int for webcam device index
                try:
                    source_int = int(source)
                except ValueError:
                    source_int = 0
                cap = cv2.VideoCapture(source_int)
            elif source_type == "rtsp":
                cap = cv2.VideoCapture(source)
            elif source_type == "http":
                cap = cv2.VideoCapture(source)
            elif source_type == "file":
                cap = cv2.VideoCapture(source)
            else:
                logger.error(f"Unknown source type: {source_type}")
                return False

            if not cap.isOpened():
                logger.error(f"Failed to open camera {camera_id} from source {source}")
                return False

            self.active_streams[camera_id] = cap
            logger.info(f"Camera {camera_id} opened successfully")
            return True

        except Exception as e:
            logger.error(f"Error opening camera {camera_id}: {e}")
            return False

    def close_camera(self, camera_id: int) -> None:
        """
        Close camera stream
        """
        if camera_id in self.active_streams:
            self.active_streams[camera_id].release()
            del self.active_streams[camera_id]
            logger.info(f"Camera {camera_id} closed")

        if camera_id in self.stream_tasks:
            self.stream_tasks[camera_id].cancel()
            del self.stream_tasks[camera_id]

    async def read_frame(
        self,
        camera_id: int,
        detection_enabled: bool = True,
        confidence_threshold: float = 0.5
    ) -> Optional[Dict]:
        """
        Read and process a single frame from camera
        """
        if camera_id not in self.active_streams:
            return None

        cap = self.active_streams[camera_id]

        # Read frame in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        ret, frame = await loop.run_in_executor(None, cap.read)

        if not ret:
            logger.warning(f"Failed to read frame from camera {camera_id}")
            return None

        detections = []

        # Run detection if enabled
        if detection_enabled:
            detections = await detection_service.detect_frame_async(
                frame,
                confidence_threshold
            )

            # Draw detections on frame
            if detections:
                frame = detection_service.draw_detections(frame, detections)

        # Encode frame to JPEG
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        frame_base64 = base64.b64encode(buffer).decode('utf-8')

        return {
            "camera_id": camera_id,
            "frame_data": frame_base64,
            "detections": detections,
            "timestamp": datetime.utcnow().isoformat(),
            "has_suspicious_activity": detection_service.is_suspicious_behavior(detections)
        }

    async def stream_frames(
        self,
        camera_id: int,
        detection_enabled: bool = True,
        confidence_threshold: float = 0.5,
        fps: int = 30
    ) -> AsyncGenerator[Dict, None]:
        """
        Continuously stream frames from camera
        """
        frame_delay = 1.0 / fps

        while camera_id in self.active_streams:
            frame_data = await self.read_frame(
                camera_id,
                detection_enabled,
                confidence_threshold
            )

            if frame_data:
                yield frame_data

            await asyncio.sleep(frame_delay)

    def close_all_cameras(self) -> None:
        """
        Close all active camera streams
        """
        camera_ids = list(self.active_streams.keys())
        for camera_id in camera_ids:
            self.close_camera(camera_id)


# Global instance
camera_service = CameraStreamService()
