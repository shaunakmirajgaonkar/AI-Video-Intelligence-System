"""
main.py — AI Video Intelligence System
100% Local · OpenCV + YOLOv8 + Ollama (moondream / llava)

Usage:
    python3 main.py                          # webcam
    python3 main.py --source video.mp4       # video file
    python3 main.py --source rtsp://...      # IP camera
    python3 main.py --source 0 --save        # webcam + record
"""

import sys
import time
import argparse
from datetime import datetime

import cv2

from config import SUMMARY_INTERVAL, DEFAULT_REPORT, VIDEO_FPS
from core   import Detector, ActivityRecogniser, SceneSummariser, Analytics
from utils  import draw_box, draw_hud, save_report, print_summary


# ─────────────────────────────────────────────────────────────────────────────

def build_writer(cap: cv2.VideoCapture, path: str) -> cv2.VideoWriter:
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    return cv2.VideoWriter(path, fourcc, VIDEO_FPS, (w, h))


def run(source, save_video: bool = False, report_path: str = DEFAULT_REPORT) -> None:

    # ── initialise components ──────────────────────────────────────────
    detector   = Detector()
    recogniser = ActivityRecogniser()
    summariser = SceneSummariser()
    analytics  = Analytics()

    # ── open video source ──────────────────────────────────────────────
    src = int(source) if str(source).isdigit() else source
    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        sys.exit(f"❌  Cannot open source: {source}")

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"🎥  Stream: {w}×{h}  |  source={source}")

    writer = None
    if save_video:
        vpath  = f"output_{datetime.now().strftime('%H%M%S')}.mp4"
        writer = build_writer(cap, vpath)
        print(f"💾  Recording → {vpath}")

    # ── main loop ──────────────────────────────────────────────────────
    last_summary_t = time.time()
    prev_t         = time.time()
    print("▶   Running — press  Q  to quit\n")

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        detections = detector.detect(frame)

        activity_map: dict[int, str] = {}
        for d in detections:
            act = recogniser.update(d["id"], d["bbox"])
            activity_map[d["id"]] = act
            draw_box(frame, d, act)

        now    = time.time()
        dt     = now - prev_t
        prev_t = now
        analytics.update(detections, activity_map, dt)

        if now - last_summary_t >= SUMMARY_INTERVAL:
            summariser.summarise_async(frame)
            last_summary_t = now
            analytics.log_event(f"Scene summarised at frame {analytics.total_frames}")

        draw_hud(frame, analytics, summariser.last_summary)

        if writer:
            writer.write(frame)
        cv2.imshow("AI Video Intelligence System", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            analytics.log_event("User quit")
            break

    cap.release()
    if writer:
        writer.release()
    cv2.destroyAllWindows()

    print_summary(analytics, summariser.last_summary)
    save_report(analytics, summariser.last_summary, report_path)


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="AI Video Intelligence System (100% Local)")
    ap.add_argument("--source", default="0",
                    help="0=webcam | path/to/video.mp4 | rtsp://...")
    ap.add_argument("--save",   action="store_true", help="Record output as MP4")
    ap.add_argument("--report", default=DEFAULT_REPORT, help="JSON report output path")
    args = ap.parse_args()
    run(source=args.source, save_video=args.save, report_path=args.report)