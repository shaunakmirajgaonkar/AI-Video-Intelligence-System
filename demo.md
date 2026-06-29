# Demo Guide

## Running a Demo

### 1. Webcam Demo
```bash
python3 main.py
```
- Sit in front of your webcam
- Move around to trigger different activity labels
- Bring objects into frame (phone, bottle, book) to see multi-class detection
- Wait 10 seconds for the first AI scene summary at the bottom

### 2. Video File Demo
```bash
python3 main.py --source your_video.mp4 --save
```
- Processes any MP4/AVI/MOV file
- Saves annotated output as `output_HHMMSS.mp4`

### 3. What to Show in a Demo Recording

| Timestamp | Action | Expected Output |
|---|---|---|
| 0:00 | Sit still | `person [stationary]` |
| 0:10 | Scene summary fires | Bottom bar updates with AI description |
| 0:20 | Wave / move arms | `person [moving]` |
| 0:35 | Stand and walk | `person [walking]` |
| 0:50 | Bring phone into frame | `person: 1, cell phone: 1` in HUD |
| 1:00 | Press Q | Terminal shows SESSION SUMMARY + report.json saved |

### 4. Screen Recording on Mac
```
Cmd + Shift + 5 → Select area → Record
```

## Sample Terminal Output
```
🔵 Loading YOLO model: yolov8n.pt
🎥  Stream: 1920×1080  |  source=0
▶   Running — press  Q  to quit

──────────────────────────────────────────────────
  SESSION SUMMARY
──────────────────────────────────────────────────
  Total frames     : 1842
  Total detections : 1956
  Avg det/frame    : 1.06
  Object counts    : {'person': 1, 'clock': 1}
  Scene summary    : A person wearing glasses sits at a desk
                     with a clock visible on the shelf.
──────────────────────────────────────────────────
📄 Report saved → /Users/shaunak/ai_video_intelligence_/report.json
```
