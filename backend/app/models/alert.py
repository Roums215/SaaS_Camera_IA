from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class AlertSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(str, enum.Enum):
    PENDING = "pending"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    FALSE_ALARM = "false_alarm"


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    # Related detection
    detection_id = Column(Integer, ForeignKey("detections.id"), nullable=False)

    # User to notify
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Alert details
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    severity = Column(SQLEnum(AlertSeverity), default=AlertSeverity.MEDIUM)
    status = Column(SQLEnum(AlertStatus), default=AlertStatus.PENDING)

    # Notification status
    notified = Column(Boolean, default=False)
    notification_sent_at = Column(DateTime(timezone=True), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    detection = relationship("Detection", back_populates="alerts")
    user = relationship("User", back_populates="alerts")

    def __repr__(self):
        return f"<Alert {self.id} - {self.severity}>"
