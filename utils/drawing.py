"""
utils/drawing.py — OpenCV drawing helpers: bounding boxes and HUD overlay
"""

import cv2
from config import PALETTE, HUD_WIDTH


# ── Bounding box ─────────────────────────────────────────────────────────────

def draw_box(frame, detection: dict, activity: str) -> None:
    """Draw a labelled bounding box for one detection."""
    x1, y1, x2, y2 = map(int, detection["bbox"])
    color = PALETTE.get(detection["label"], PALETTE["default"])

    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    tag = f"{detection['label']} [{activity}]"
    (tw, th), _ = cv2.getTextSize(tag, cv2.FONT_HERSHEY_SIMPLEX, 0.46, 1)
    cv2.rectangle(frame, (x1, y1 - th - 6), (x1 + tw + 6, y1), color, -1)
    cv2.putText(frame, tag, (x1 + 3, y1 - 4),
                cv2.FONT_HERSHEY_SIMPLEX, 0.46, (0, 0, 0), 1, cv2.LINE_AA)


# ── HUD sidebar ──────────────────────────────────────────────────────────────

def draw_hud(frame, analytics, summary: str) -> None:
    """Draw the left-side info panel and bottom scene summary bar."""
    h, w = frame.shape[:2]

    # ── sidebar background ──
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (HUD_WIDTH, h), (15, 15, 25), -1)
    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)

    y = _line(frame, "AI VIDEO INTELLIGENCE", 8, 28,
              scale=0.52, color=(80, 200, 255), font=cv2.FONT_HERSHEY_DUPLEX)
    y = _line(frame, f"FPS : {analytics.fps:.1f}", 8, y + 6,
              scale=0.42, color=(180, 180, 180))
    y = _line(frame, f"Frames: {analytics.total_frames}", 8, y + 2,
              scale=0.40, color=(150, 150, 150))

    # detections
    y = _section(frame, "DETECTIONS", y + 14)
    for label, cnt in sorted(analytics.counts.items()):
        y = _line(frame, f"  {label}: {cnt}", 8, y + 18, scale=0.42)

    # activities
    y = _section(frame, "ACTIVITIES", y + 14)
    shown = set()
    for tid, act in list(analytics.activities.items())[:8]:
        if act not in shown:
            y = _line(frame, f"  id{tid}: {act}", 8, y + 18,
                      scale=0.40, color=(200, 255, 180))
            shown.add(act)

    # ── bottom summary bar ──
    lines  = _wrap(summary, 62)
    bar_h  = 16 * (len(lines) + 1) + 8
    sy_top = h - bar_h
    cv2.rectangle(frame, (0, sy_top), (w, h), (12, 12, 22), -1)
    _line(frame, "[ SCENE ]", HUD_WIDTH + 8, sy_top + 14,
          scale=0.42, color=(80, 200, 255))
    sy = sy_top + 28
    for line in lines:
        _line(frame, line, HUD_WIDTH + 8, sy, scale=0.40, color=(220, 220, 200))
        sy += 16


# ── helpers ──────────────────────────────────────────────────────────────────

def _line(frame, text: str, x: int, y: int,
          scale: float = 0.42,
          color: tuple  = (220, 220, 220),
          font: int     = cv2.FONT_HERSHEY_SIMPLEX) -> int:
    cv2.putText(frame, text, (x, y), font, scale, color, 1, cv2.LINE_AA)
    return y


def _section(frame, title: str, y: int) -> int:
    cv2.putText(frame, f"[ {title} ]", (8, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.42, (80, 200, 255), 1, cv2.LINE_AA)
    return y


def _wrap(text: str, width: int) -> list[str]:
    words  = text.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines or [""]
