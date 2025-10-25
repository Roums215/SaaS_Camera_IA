from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.camera import Camera
from app.models.detection import Detection
from app.schemas.camera import CameraCreate, CameraUpdate, CameraResponse, CameraStats
from app.services.camera_service import camera_service

router = APIRouter()


@router.post("/", response_model=CameraResponse, status_code=status.HTTP_201_CREATED)
async def create_camera(
    camera_in: CameraCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new camera
    """
    camera = Camera(
        **camera_in.model_dump(),
        owner_id=current_user.id
    )

    db.add(camera)
    db.commit()
    db.refresh(camera)

    return camera


@router.get("/", response_model=List[CameraResponse])
async def list_cameras(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    List all cameras for current user
    """
    cameras = db.query(Camera).filter(
        Camera.owner_id == current_user.id
    ).offset(skip).limit(limit).all()

    return cameras


@router.get("/{camera_id}", response_model=CameraResponse)
async def get_camera(
    camera_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get camera by ID
    """
    camera = db.query(Camera).filter(
        Camera.id == camera_id,
        Camera.owner_id == current_user.id
    ).first()

    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )

    return camera


@router.put("/{camera_id}", response_model=CameraResponse)
async def update_camera(
    camera_id: int,
    camera_in: CameraUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update camera
    """
    camera = db.query(Camera).filter(
        Camera.id == camera_id,
        Camera.owner_id == current_user.id
    ).first()

    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )

    # Update camera fields
    update_data = camera_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(camera, field, value)

    camera.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(camera)

    return camera


@router.delete("/{camera_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_camera(
    camera_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete camera
    """
    camera = db.query(Camera).filter(
        Camera.id == camera_id,
        Camera.owner_id == current_user.id
    ).first()

    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )

    # Close camera stream if active
    camera_service.close_camera(camera_id)

    db.delete(camera)
    db.commit()


@router.post("/{camera_id}/start")
async def start_camera(
    camera_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Start camera stream
    """
    camera = db.query(Camera).filter(
        Camera.id == camera_id,
        Camera.owner_id == current_user.id
    ).first()

    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )

    # Open camera stream
    success = camera_service.open_camera(
        camera_id,
        camera.source,
        camera.source_type
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start camera stream"
        )

    camera.is_active = True
    db.commit()

    return {"message": "Camera started successfully"}


@router.post("/{camera_id}/stop")
async def stop_camera(
    camera_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Stop camera stream
    """
    camera = db.query(Camera).filter(
        Camera.id == camera_id,
        Camera.owner_id == current_user.id
    ).first()

    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )

    # Close camera stream
    camera_service.close_camera(camera_id)

    camera.is_active = False
    db.commit()

    return {"message": "Camera stopped successfully"}


@router.get("/{camera_id}/stats", response_model=CameraStats)
async def get_camera_stats(
    camera_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get camera statistics
    """
    camera = db.query(Camera).filter(
        Camera.id == camera_id,
        Camera.owner_id == current_user.id
    ).first()

    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )

    # Total detections
    total_detections = db.query(func.count(Detection.id)).filter(
        Detection.camera_id == camera_id
    ).scalar()

    # Detections today
    today = datetime.utcnow().date()
    detections_today = db.query(func.count(Detection.id)).filter(
        Detection.camera_id == camera_id,
        func.date(Detection.created_at) == today
    ).scalar()

    # Average confidence
    avg_confidence = db.query(func.avg(Detection.confidence)).filter(
        Detection.camera_id == camera_id
    ).scalar()

    return {
        "camera_id": camera_id,
        "total_detections": total_detections or 0,
        "detections_today": detections_today or 0,
        "last_detection": camera.last_detection,
        "average_confidence": float(avg_confidence) if avg_confidence else None
    }
