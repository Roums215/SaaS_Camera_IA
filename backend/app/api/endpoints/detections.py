from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.camera import Camera
from app.models.detection import Detection
from app.schemas.detection import DetectionCreate, DetectionUpdate, DetectionResponse

router = APIRouter()


@router.post("/", response_model=DetectionResponse, status_code=status.HTTP_201_CREATED)
async def create_detection(
    detection_in: DetectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new detection
    """
    # Verify camera belongs to user
    camera = db.query(Camera).filter(
        Camera.id == detection_in.camera_id,
        Camera.owner_id == current_user.id
    ).first()

    if not camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Camera not found"
        )

    detection = Detection(**detection_in.model_dump())
    db.add(detection)

    # Update camera last detection time
    camera.last_detection = datetime.utcnow()

    db.commit()
    db.refresh(detection)

    return detection


@router.get("/", response_model=List[DetectionResponse])
async def list_detections(
    skip: int = 0,
    limit: int = 100,
    camera_id: Optional[int] = None,
    detection_type: Optional[str] = None,
    min_confidence: Optional[float] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    List detections with filters
    """
    # Get user's camera IDs
    camera_ids = db.query(Camera.id).filter(
        Camera.owner_id == current_user.id
    ).all()
    camera_ids = [cid[0] for cid in camera_ids]

    # Build query
    query = db.query(Detection).filter(Detection.camera_id.in_(camera_ids))

    if camera_id:
        query = query.filter(Detection.camera_id == camera_id)

    if detection_type:
        query = query.filter(Detection.detection_type == detection_type)

    if min_confidence:
        query = query.filter(Detection.confidence >= min_confidence)

    if start_date:
        query = query.filter(Detection.created_at >= start_date)

    if end_date:
        query = query.filter(Detection.created_at <= end_date)

    detections = query.order_by(Detection.created_at.desc()).offset(skip).limit(limit).all()

    return detections


@router.get("/{detection_id}", response_model=DetectionResponse)
async def get_detection(
    detection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get detection by ID
    """
    detection = db.query(Detection).filter(Detection.id == detection_id).first()

    if not detection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Detection not found"
        )

    # Verify user owns the camera
    camera = db.query(Camera).filter(
        Camera.id == detection.camera_id,
        Camera.owner_id == current_user.id
    ).first()

    if not camera:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this detection"
        )

    return detection


@router.put("/{detection_id}", response_model=DetectionResponse)
async def update_detection(
    detection_id: int,
    detection_in: DetectionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update detection (mark as reviewed, false positive, etc.)
    """
    detection = db.query(Detection).filter(Detection.id == detection_id).first()

    if not detection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Detection not found"
        )

    # Verify user owns the camera
    camera = db.query(Camera).filter(
        Camera.id == detection.camera_id,
        Camera.owner_id == current_user.id
    ).first()

    if not camera:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this detection"
        )

    # Update detection
    update_data = detection_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(detection, field, value)

    db.commit()
    db.refresh(detection)

    return detection


@router.delete("/{detection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_detection(
    detection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete detection
    """
    detection = db.query(Detection).filter(Detection.id == detection_id).first()

    if not detection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Detection not found"
        )

    # Verify user owns the camera
    camera = db.query(Camera).filter(
        Camera.id == detection.camera_id,
        Camera.owner_id == current_user.id
    ).first()

    if not camera:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this detection"
        )

    db.delete(detection)
    db.commit()


@router.get("/stats/summary")
async def get_detection_stats(
    days: int = Query(default=7, ge=1, le=90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get detection statistics summary
    """
    # Get user's camera IDs
    camera_ids = db.query(Camera.id).filter(
        Camera.owner_id == current_user.id
    ).all()
    camera_ids = [cid[0] for cid in camera_ids]

    start_date = datetime.utcnow() - timedelta(days=days)

    # Total detections
    total_detections = db.query(func.count(Detection.id)).filter(
        Detection.camera_id.in_(camera_ids),
        Detection.created_at >= start_date
    ).scalar()

    # Detections by type
    detections_by_type = db.query(
        Detection.detection_type,
        func.count(Detection.id)
    ).filter(
        Detection.camera_id.in_(camera_ids),
        Detection.created_at >= start_date
    ).group_by(Detection.detection_type).all()

    # Average confidence
    avg_confidence = db.query(func.avg(Detection.confidence)).filter(
        Detection.camera_id.in_(camera_ids),
        Detection.created_at >= start_date
    ).scalar()

    # False positives rate
    false_positives = db.query(func.count(Detection.id)).filter(
        Detection.camera_id.in_(camera_ids),
        Detection.created_at >= start_date,
        Detection.is_false_positive == True
    ).scalar()

    return {
        "total_detections": total_detections or 0,
        "detections_by_type": dict(detections_by_type),
        "average_confidence": float(avg_confidence) if avg_confidence else 0.0,
        "false_positives": false_positives or 0,
        "false_positive_rate": (false_positives / total_detections * 100) if total_detections else 0.0,
        "period_days": days
    }
