from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.alert import AlertSeverity, AlertStatus


class AlertBase(BaseModel):
    title: str
    message: str
    severity: AlertSeverity = AlertSeverity.MEDIUM


class AlertCreate(AlertBase):
    detection_id: int
    user_id: int


class AlertUpdate(BaseModel):
    status: Optional[AlertStatus] = None
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None


class AlertResponse(AlertBase):
    id: int
    detection_id: int
    user_id: int
    status: AlertStatus
    notified: bool
    notification_sent_at: Optional[datetime] = None
    created_at: datetime
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True
