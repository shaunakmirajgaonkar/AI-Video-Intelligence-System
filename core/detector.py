"""
core/detector.py — YOLOv8 object detector + tracker wrapper
"""

from ultralytics import YOLO
from config import YOLO_MODEL, CONF_THRESHOLD, TRACK_PERSIST


class Detector:
    """
    Thin wrapper around Ultralytics YOLOv8.
    Downloads the model weights on first use automatically.
    """

    def __init__(self,
                 model_path: str  = YOLO_MODEL,
                 conf: float      = CONF_THRESHOLD,
                 persist: bool    = TRACK_PERSIST):
        print(f"🔵 Loading YOLO model: {model_path}")
        self._model   = YOLO(model_path)
        self._conf    = conf
        self._persist = persist

    # ── public ──────────────────────────────────────────────────────────

    def detect(self, frame) -> list[dict]:
        """
        Run detection + tracking on a single frame.

        Returns a list of dicts:
            {
                "id":    int,    # persistent track ID
                "label": str,    # COCO class name
                "conf":  float,  # confidence 0-1
                "bbox":  [x1, y1, x2, y2],
            }
        """
        results = self._model.track(
            frame,
            persist=self._persist,
            conf=self._conf,
            verbose=False,
        )

        detections = []
        if not results or results[0].boxes is None:
            return detections

        boxes = results[0].boxes
        for i, box in enumerate(boxes):
            xyxy  = box.xyxy[0].tolist()
            conf  = float(box.conf[0])
            cls   = int(box.cls[0])
            label = self._model.names[cls]
            tid   = int(box.id[0]) if box.id is not None else i

            detections.append({
                "id":    tid,
                "label": label,
                "conf":  round(conf, 3),
                "bbox":  xyxy,
            })

        return detections

    @property
    def class_names(self) -> dict:
        return self._model.names