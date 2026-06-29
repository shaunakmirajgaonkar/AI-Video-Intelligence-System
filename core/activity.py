"""
core/activity.py — Rule-based activity recognition from bounding-box motion
"""

from collections import defaultdict, deque
from config import ACTIVITY_WINDOW


class ActivityRecogniser:
    """
    Tracks centroid history per object ID and classifies motion.

    Labels returned:
        initialising  — not enough history yet
        stationary    — barely moved
        moving        — slow/ambiguous movement
        walking       — moderate displacement
        running       — large displacement
    """

    THRESHOLDS = {
        "stationary": 5,
        "moving":     30,
        "walking":    80,
        # > walking → running
    }

    def __init__(self, window: int = ACTIVITY_WINDOW):
        self._history: dict[int, deque] = defaultdict(
            lambda: deque(maxlen=window)
        )

    # ── public ──────────────────────────────────────────────────────────

    def update(self, track_id: int, bbox: list[float]) -> str:
        """Feed a new bounding box and return the current activity label."""
        cx = (bbox[0] + bbox[2]) / 2
        cy = (bbox[1] + bbox[3]) / 2
        self._history[track_id].append((cx, cy))
        return self._classify(track_id)

    def reset(self, track_id: int) -> None:
        """Clear history for a specific ID (e.g. when a track is lost)."""
        self._history.pop(track_id, None)

    def clear(self) -> None:
        """Clear all history."""
        self._history.clear()

    # ── private ─────────────────────────────────────────────────────────

    def _classify(self, track_id: int) -> str:
        pts = self._history[track_id]
        if len(pts) < 5:
            return "initialising"

        dx   = pts[-1][0] - pts[0][0]
        dy   = pts[-1][1] - pts[0][1]
        dist = (dx ** 2 + dy ** 2) ** 0.5

        t = self.THRESHOLDS
        if dist < t["stationary"]:
            return "stationary"
        if dist < t["moving"]:
            return "moving"
        if dist < t["walking"]:
            return "walking"
        return "running"