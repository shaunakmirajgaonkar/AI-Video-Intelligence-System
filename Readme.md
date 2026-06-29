# 🟣 AI Video Intelligence System

> **100% Local · No Cloud · No API Costs · Real-time Computer Vision**

A production-ready AI platform that automatically understands and analyzes video streams in real time using object detection, activity recognition, and AI-powered scene summarization — all running locally on your machine.

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-purple?style=flat-square)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-black?style=flat-square)
![OpenCV](https://img.shields.io/badge/OpenCV-4.9-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 🎯 Core Features

| Feature | Description |
|---|---|
| 🔍 **Object Detection** | 80 COCO classes via YOLOv8n at 25–30 FPS |
| 🏃 **Activity Recognition** | Stationary / Moving / Walking / Running per tracked ID |
| 🧠 **Scene Summarisation** | Local LLM (moondream) describes scene every N seconds |
| 📊 **Live HUD Overlay** | FPS, object counts, activity map on video frame |
| 📄 **JSON Report** | Auto-saved on exit with full event log and statistics |
| 🎥 **Multi-source Input** | Webcam, video file, RTSP/IP camera |
| 💾 **Video Recording** | Optional MP4 output of annotated session |

---

## 🗂️ Project Structure

```
ai-video-intelligence/
├── main.py                  # Entry point — video pipeline loop
├── config.py                # All tuneable constants
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
│
├── core/
│   ├── __init__.py
│   ├── detector.py          # YOLOv8 object detector + ByteTrack wrapper
│   ├── activity.py          # Rule-based motion activity classifier
│   ├── summariser.py        # Async Ollama LLM scene summariser
│   └── analytics.py        # Real-time stats, FPS, event logger
│
├── utils/
│   ├── __init__.py
│   ├── drawing.py           # OpenCV bounding boxes + HUD rendering
│   └── report.py            # JSON report writer + terminal summary
│
└── doc/
    ├── ARCHITECTURE.md      # System design and data flow
    └── DEMO.md              # Screenshots and demo instructions
```

---

## ⚡ Quick Start

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com) installed

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/shaunakmirajgaonkar/ai-video-intelligence.git
cd ai-video-intelligence

# 2. Install Python dependencies
pip3 install -r requirements.txt

# 3. Pull the vision model (one time, ~1.7 GB)
ollama pull moondream

# 4. Run
python3 main.py
```

### Usage

```bash
python3 main.py                          # Webcam (default)
python3 main.py --source video.mp4       # Video file
python3 main.py --source rtsp://ip/stream  # IP camera / RTSP
python3 main.py --source 0 --save        # Webcam + record MP4
python3 main.py --report my_report.json  # Custom report path
```

### Controls
| Key | Action |
|---|---|
| `Q` | Quit and save report |

---

## 🖥️ Live Output

```
┌──────────────────────┬────────────────────────────────────┐
│ AI VIDEO INTELLIGENCE│                                    │
│ FPS : 28.4           │                                    │
│ Frames: 1842         │     ┌─────────────────┐           │
│                      │     │  person         │           │
│ [ DETECTIONS ]       │     │  [stationary]   │           │
│   person: 1          │     └─────────────────┘           │
│   clock: 1           │                                    │
│                      │                                    │
│ [ ACTIVITIES ]       │                                    │
│   id1: stationary    │                                    │
├──────────────────────┴────────────────────────────────────┤
│ [ SCENE ] A person wearing glasses is sitting at a desk   │
│ with a clock visible on the shelf behind them.            │
└───────────────────────────────────────────────────────────┘
```

---

## 🔧 Configuration

Edit `config.py` to tune the system:

```python
YOLO_MODEL       = "yolov8n.pt"   # n=fastest | s/m/l/x=more accurate
OLLAMA_MODEL     = "moondream"    # moondream | llava | llava:13b
SUMMARY_INTERVAL = 10             # seconds between AI scene summaries
CONF_THRESHOLD   = 0.45           # detection confidence threshold
MAX_SUMMARY_TOKENS = 120          # keeps LLM token usage minimal
```

---

## 🏗️ Architecture

```
Video Source (webcam / file / RTSP)
        │
        ▼
  YOLOv8n (Ultralytics)          ← detect 80 classes + ByteTrack IDs
        │
        ├──► ActivityRecogniser   ← rule-based motion: stationary/walking/running
        │
        ├──► Analytics Tracker    ← counts, FPS, event log
        │
        ├──► SceneSummariser      ← async thread → Ollama moondream/llava
        │       (fires every N seconds, max 120 tokens)
        │
        └──► OpenCV HUD + Display
                        │
                        └──► report.json on exit
```

---

## 🛠️ Tech Stack

- **[Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)** — Object detection & tracking
- **[Ollama](https://ollama.com)** — Local LLM inference server
- **[moondream](https://ollama.com/library/moondream)** — Lightweight vision language model
- **[OpenCV](https://opencv.org)** — Video I/O and frame rendering
- **Python 3.12** — Core language

---

## 📄 Sample Report Output

```json
{
  "session": {
    "timestamp": "2026-06-29T13:30:00",
    "saved_to": "/Users/shaunak/ai_video_intelligence_/report.json"
  },
  "stats": {
    "total_frames": 1842,
    "total_detections": 1956,
    "avg_detections_per_frame": 1.06,
    "final_counts": { "person": 1, "clock": 1 },
    "events": [
      { "time": "2026-06-29T13:25:10", "frame": 300, "event": "Scene summarised at frame 300" },
      { "time": "2026-06-29T13:30:00", "frame": 1842, "event": "User quit" }
    ]
  },
  "last_scene_summary": "A person wearing glasses is sitting at a desk with a clock on the shelf."
}
```

---

## 👤 Author

**Shaunak Mirajgaonkar**
- GitHub: [@shaunakmirajgaonkar](https://github.com/shaunakmirajgaonkar)
- BE Computer Engineering, MMCOE Pune

---

## 📜 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
