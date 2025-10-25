from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class DetectionBase(BaseModel):
    detection_type: str = "shoplifting"
    confidence: float = Field(..., ge=0.0, le=1.0)


class DetectionCreate(DetectionBase):
    camera_id: int
    bbox_x1: Optional[float] = None
    bbox_y1: Optional[float] = None
    bbox_x2: Optional[float] = None
    bbox_y2: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None
    image_path: Optional[str] = None
    video_path: Optional[str] = None


class DetectionUpdate(BaseModel):
    is_false_positive: Optional[bool] = None
    reviewed: Optional[bool] = None


class DetectionResponse(DetectionBase):
    id: int
    camera_id: int
    bbox_x1: Optional[float] = None
    bbox_y1: Optional[float] = None
    bbox_x2: Optional[float] = None
    bbox_y2: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None
    image_path: Optional[str] = None
    video_path: Optional[str] = None
    is_false_positive: bool
    reviewed: bool
    created_at: datetime

    class Config:
        from_attributes = True


class DetectionFrame(BaseModel):
    """Frame data for WebSocket streaming"""
    camera_id: int
    frame_data: str  # Base64 encoded image
    detections: list[Dict[str, Any]]
    timestamp: datetime
