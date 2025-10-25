from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)

    # Camera reference
    camera_id = Column(Integer, ForeignKey("cameras.id"), nullable=False)

    # Detection info
    detection_type = Column(String, default="shoplifting")  # shoplifting, suspicious_behavior, etc.
    confidence = Column(Float, nullable=False)

    # Bounding box coordinates
    bbox_x1 = Column(Float, nullable=True)
    bbox_y1 = Column(Float, nullable=True)
    bbox_x2 = Column(Float, nullable=True)
    bbox_y2 = Column(Float, nullable=True)

    # Additional metadata
    metadata = Column(JSON, nullable=True)

    # Image/Video reference
    image_path = Column(String, nullable=True)
    video_path = Column(String, nullable=True)

    # Validation
    is_false_positive = Column(Boolean, default=False)
    reviewed = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    camera = relationship("Camera", back_populates="detections")
    alerts = relationship("Alert", back_populates="detection", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Detection {self.id} - {self.detection_type}>"
