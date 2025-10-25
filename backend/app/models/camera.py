from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # Camera source (URL, device index, etc.)
    source = Column(String, nullable=False)
    source_type = Column(String, default="webcam")  # webcam, rtsp, http, file

    # Settings
    is_active = Column(Boolean, default=True)
    fps = Column(Integer, default=30)
    resolution_width = Column(Integer, default=1920)
    resolution_height = Column(Integer, default=1080)

    # Detection settings
    detection_enabled = Column(Boolean, default=True)
    confidence_threshold = Column(Float, default=0.5)
    alert_cooldown_seconds = Column(Integer, default=60)

    # Owner
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_detection = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    owner = relationship("User", back_populates="cameras")
    detections = relationship("Detection", back_populates="camera", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Camera {self.name}>"
