import cv2
import numpy as np
from ultralytics import YOLO
from typing import List, Tuple, Optional, Dict, Any
import logging
from pathlib import Path
import asyncio
from concurrent.futures import ThreadPoolExecutor

from app.core.config import settings

logger = logging.getLogger(__name__)


class DetectionService:
    """YOLOv8 Shoplifting Detection Service"""

    def __init__(self):
        self.model: Optional[YOLO] = None
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.model_loaded = False

    def load_model(self) -> bool:
        """Load YOLOv8 model"""
        try:
            model_path = Path(settings.MODEL_PATH)

            if not model_path.exists():
                logger.warning(f"Model not found at {model_path}. Using default YOLOv8n.")
                # Use default YOLOv8 nano model for object detection
                self.model = YOLO('yolov8n.pt')
            else:
                self.model = YOLO(str(model_path))

            self.model_loaded = True
            logger.info("YOLOv8 model loaded successfully")
            return True

        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False

    async def detect_frame_async(
        self,
        frame: np.ndarray,
        confidence_threshold: float = None
    ) -> List[Dict[str, Any]]:
        """
        Async wrapper for frame detection
        """
        if confidence_threshold is None:
            confidence_threshold = settings.CONFIDENCE_THRESHOLD

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            self._detect_frame_sync,
            frame,
            confidence_threshold
        )

    def _detect_frame_sync(
        self,
        frame: np.ndarray,
        confidence_threshold: float
    ) -> List[Dict[str, Any]]:
        """
        Synchronous frame detection
        """
        if not self.model_loaded:
            if not self.load_model():
                return []

        try:
            # Run inference
            results = self.model(
                frame,
                conf=confidence_threshold,
                iou=settings.IOU_THRESHOLD,
                verbose=False
            )

            detections = []

            for result in results:
                boxes = result.boxes

                for box in boxes:
                    # Get box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

                    # Get confidence and class
                    confidence = float(box.conf[0].cpu().numpy())
                    class_id = int(box.cls[0].cpu().numpy())
                    class_name = self.model.names[class_id]

                    # For shoplifting detection, we focus on person class
                    # and suspicious behaviors (can be customized)
                    detection_type = "person_detected"

                    # If using custom trained model, it might have specific classes
                    if hasattr(self.model, 'names') and 'shoplifting' in str(self.model.names).lower():
                        detection_type = class_name

                    detections.append({
                        "bbox": {
                            "x1": float(x1),
                            "y1": float(y1),
                            "x2": float(x2),
                            "y2": float(y2)
                        },
                        "confidence": confidence,
                        "class_id": class_id,
                        "class_name": class_name,
                        "detection_type": detection_type
                    })

            return detections

        except Exception as e:
            logger.error(f"Error during detection: {e}")
            return []

    def draw_detections(
        self,
        frame: np.ndarray,
        detections: List[Dict[str, Any]]
    ) -> np.ndarray:
        """
        Draw bounding boxes and labels on frame
        """
        annotated_frame = frame.copy()

        for detection in detections:
            bbox = detection["bbox"]
            confidence = detection["confidence"]
            class_name = detection["class_name"]

            # Draw bounding box
            x1, y1 = int(bbox["x1"]), int(bbox["y1"])
            x2, y2 = int(bbox["x2"]), int(bbox["y2"])

            # Color based on detection type (red for suspicious)
            color = (0, 0, 255) if "suspicious" in class_name.lower() else (0, 255, 0)

            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)

            # Draw label
            label = f"{class_name}: {confidence:.2f}"
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            cv2.rectangle(
                annotated_frame,
                (x1, y1 - label_size[1] - 10),
                (x1 + label_size[0], y1),
                color,
                -1
            )
            cv2.putText(
                annotated_frame,
                label,
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2
            )

        return annotated_frame

    def is_suspicious_behavior(self, detections: List[Dict[str, Any]]) -> bool:
        """
        Analyze detections to determine if behavior is suspicious
        This is a simplified version - can be enhanced with:
        - Temporal analysis (tracking over time)
        - Pose estimation
        - Action recognition
        """
        # Simple heuristic: high confidence person detections in restricted areas
        for detection in detections:
            if detection["confidence"] > 0.7:
                # Custom logic based on your shoplifting detection model
                if "shoplifting" in detection.get("detection_type", "").lower():
                    return True
                # Or based on specific class names
                if detection.get("class_name", "") in ["suspicious_person", "theft"]:
                    return True

        return False


# Global instance
detection_service = DetectionService()
