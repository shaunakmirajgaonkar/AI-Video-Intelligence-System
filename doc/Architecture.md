# System Architecture

## Data Flow

```
Video Source (webcam / file / RTSP)
        │
        ▼
  cv2.VideoCapture
        │
        ▼
  ┌─────────────────────────────────────┐
  │         main.py — Video Loop        │
  └──────────────┬──────────────────────┘
                 │
        ┌────────▼────────┐
        │   Detector       │  core/detector.py
        │   YOLOv8n        │  → detect() returns list[dict]
        │   + ByteTrack    │  → {id, label, conf, bbox}
        └────────┬─────────┘
                 │
        ┌────────▼────────┐
        │ ActivityRecog.  │  core/activity.py
        │ centroid history│  → stationary/moving/walking/running
        └────────┬─────────┘
                 │
        ┌────────▼────────┐
        │   Analytics     │  core/analytics.py
        │   counts, FPS   │  → rolling stats per frame
        │   event log     │
        └────────┬─────────┘
                 │
        ┌────────▼────────┐
        │ SceneSummariser │  core/summariser.py
        │ async thread    │  → Ollama HTTP POST every N seconds
        │ moondream/llava │  → last_summary string
        └────────┬─────────┘
                 │
        ┌────────▼────────┐
        │  draw_box()     │  utils/drawing.py
        │  draw_hud()     │  → annotated frame
        └────────┬─────────┘
                 │
        ┌────────▼────────┐
        │ cv2.imshow()    │  display
        │ VideoWriter     │  optional MP4
        └────────┬─────────┘
                 │
              Q pressed
                 │
        ┌────────▼────────┐
        │  save_report()  │  utils/report.py → report.json
        └─────────────────┘
```

## Key Design Decisions

### 1. Async Scene Summarisation
Ollama calls run in a daemon thread so they never block the video loop. A lock prevents multiple simultaneous requests.

### 2. Rule-based Activity Recognition
No ML model needed — centroid displacement over a rolling window of frames determines activity class. Fast, explainable, zero dependencies.

### 3. Single config.py
All magic numbers live in one place. Swap models, change thresholds, adjust intervals without touching business logic.

### 4. Modular core/ and utils/
`core/` = domain logic (detection, activity, summarisation, analytics)
`utils/` = presentation (drawing, reporting)
`main.py` = thin orchestrator only
