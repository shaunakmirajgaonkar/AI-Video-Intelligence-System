"""
config.py — Central configuration for AI Video Intelligence System
"""

# ── Models ──────────────────────────────────────────────
YOLO_MODEL       = "yolov8n.pt"   # n=fastest | s/m/l/x=accurate
OLLAMA_MODEL     = "moondream"    # moondream=fast | llava=detailed
OLLAMA_URL       = "http://localhost:11434/api/generate"

# ── Detection ───────────────────────────────────────────
CONF_THRESHOLD   = 0.45
TRACK_PERSIST    = True

# ── Activity Recognition ─────────────────────────────────
ACTIVITY_WINDOW  = 30    # frames of history per tracked object

# ── Scene Summariser ─────────────────────────────────────
SUMMARY_INTERVAL   = 5   # seconds between Ollama calls
MAX_SUMMARY_TOKENS = 120   # keep token usage tiny

# ── Display ──────────────────────────────────────────────
HUD_WIDTH        = 300
FONT             = "FONT_HERSHEY_SIMPLEX"
FPS_BUFFER_SIZE  = 30

# ── Output ───────────────────────────────────────────────
DEFAULT_REPORT   = "report.json"
VIDEO_FPS        = 20

# ── Colour palette (BGR) ─────────────────────────────────
PALETTE = {
    "person":       (0,   200, 255),
    "car":          (50,  205, 50),
    "motorcycle":   (255, 165, 0),
    "bicycle":      (0,   165, 255),
    "truck":        (0,   128, 255),
    "bus":          (128, 0,   255),
    "dog":          (0,   255, 200),
    "cat":          (200, 255, 0),
    "default":      (180, 100, 255),
}