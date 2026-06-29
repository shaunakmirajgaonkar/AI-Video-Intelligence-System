"""
utils/report.py — Save JSON analytics report on session end
"""

import json
from datetime import datetime
from pathlib import Path


def save_report(analytics,
                summary: str,
                path: str = "report.json") -> None:
    """Write a JSON report summarising the session."""
    report = {
        "session": {
            "timestamp":  datetime.now().isoformat(timespec="seconds"),
            "saved_to":   str(Path(path).resolve()),
        },
        "stats":    analytics.summary_dict(),
        "last_scene_summary": summary,
    }

    Path(path).write_text(json.dumps(report, indent=2))
    print(f"\n📄 Report saved → {Path(path).resolve()}")


def print_summary(analytics, summary: str) -> None:
    """Print a brief session summary to stdout."""
    print("\n" + "─" * 50)
    print("  SESSION SUMMARY")
    print("─" * 50)
    print(f"  Total frames     : {analytics.total_frames}")
    print(f"  Total detections : {analytics.total_detections}")
    print(f"  Avg det/frame    : {analytics.avg_detections_per_frame:.2f}")
    print(f"  Object counts    : {dict(analytics.counts)}")
    print(f"  Scene summary    : {summary}")
    print("─" * 50)