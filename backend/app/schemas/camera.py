from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CameraBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    source: str
    source_type: str = Field(default="webcam")


class CameraCreate(CameraBase):
    fps: Optional[int] = 30
    resolution_width: Optional[int] = 1920
    resolution_height: Optional[int] = 1080
    confidence_threshold: Optional[float] = 0.5
    alert_cooldown_seconds: Optional[int] = 60


class CameraUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    source: Optional[str] = None
    source_type: Optional[str] = None
    is_active: Optional[bool] = None
    fps: Optional[int] = None
    resolution_width: Optional[int] = None
    resolution_height: Optional[int] = None
    detection_enabled: Optional[bool] = None
    confidence_threshold: Optional[float] = None
    alert_cooldown_seconds: Optional[int] = None


class CameraResponse(CameraBase):
    id: int
    is_active: bool
    fps: int
    resolution_width: int
    resolution_height: int
    detection_enabled: bool
    confidence_threshold: float
    alert_cooldown_seconds: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_detection: Optional[datetime] = None

    class Config:
        from_attributes = True


class CameraStats(BaseModel):
    camera_id: int
    total_detections: int
    detections_today: int
    last_detection: Optional[datetime] = None
    average_confidence: Optional[float] = None
