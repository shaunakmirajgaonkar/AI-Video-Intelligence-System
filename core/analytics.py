"""
core/analytics.py — Real-time detection analytics and event logging
"""

from collections import defaultdict, deque
from datetime import datetime
from config import FPS_BUFFER_SIZE


class Analytics:
    """
    Aggregates per-frame detection results and maintains:
        - object counts per class label
        - activity map (track_id → activity string)
        - rolling FPS estimate
        - timestamped event log
    """

    MAX_EVENTS = 500

    def __init__(self):
        self.counts:     dict[str, int] = defaultdict(int)
        self.activities: dict[int, str] = {}
        self._fps_buf    = deque(maxlen=FPS_BUFFER_SIZE)
        self.events:     list[dict]     = []

        # cumulative stats
        self.total_frames    = 0
        self.total_detections = 0

    # ── update ───────────────────────────────────────────────────────────

    def update(self,
               detections:    list[dict],
               activity_map:  dict[int, str],
               frame_dt:      float) -> None:
        """Call once per frame with detection results."""
        self.counts.clear()
        for d in detections:
            self.counts[d["label"]] += 1

        self.activities = dict(activity_map)

        self._fps_buf.append(1.0 / max(frame_dt, 1e-6))
        self.total_frames     += 1
        self.total_detections += len(detections)

    def log_event(self, message: str) -> None:
        entry = {
            "time":  datetime.now().isoformat(timespec="seconds"),
            "frame": self.total_frames,
            "event": message,
        }
        self.events.append(entry)
        if len(self.events) > self.MAX_EVENTS:
            self.events.pop(0)

    # ── computed properties ──────────────────────────────────────────────

    @property
    def fps(self) -> float:
        if not self._fps_buf:
            return 0.0
        return sum(self._fps_buf) / len(self._fps_buf)

    @property
    def avg_detections_per_frame(self) -> float:
        if self.total_frames == 0:
            return 0.0
        return self.total_detections / self.total_frames

    def summary_dict(self) -> dict:
        return {
            "total_frames":            self.total_frames,
            "total_detections":        self.total_detections,
            "avg_detections_per_frame": round(self.avg_detections_per_frame, 2),
            "final_counts":            dict(self.counts),
            "events":                  self.events[-50:],
        }