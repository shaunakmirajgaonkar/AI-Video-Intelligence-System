# Changelog

All notable changes to the AI Video Intelligence System are documented here.

---

## [1.0.0] — 2026-06-29

### 🎉 Initial Release

#### Added
- Real-time object detection using YOLOv8n (80 COCO classes)
- Multi-object tracking with persistent IDs via ByteTrack
- Rule-based activity recognition (stationary / moving / walking / running)
- Async scene summarisation using Ollama (moondream / llava)
- Live HUD overlay with FPS, detection counts, and activity map
- JSON session report auto-saved on quit
- Optional MP4 video recording of annotated sessions
- Multi-source support: webcam, video file, RTSP/IP camera
- Modular project structure: `core/` and `utils/` packages
- Central `config.py` for all tuneable parameters
- CLI with `--source`, `--save`, `--report` flags

#### Tech Stack
- Python 3.12
- Ultralytics YOLOv8
- Ollama (moondream)
- OpenCV 4.9

---

## [Unreleased]

### Planned
- [ ] Web dashboard (FastAPI + React)
- [ ] Alert system for specific object classes
- [ ] Multi-camera support
- [ ] GPU acceleration toggle
- [ ] Docker container
- [ ] REST API for remote control
