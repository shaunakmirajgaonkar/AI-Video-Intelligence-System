"""
core/summariser.py — Async Ollama scene summariser (minimal token usage)
"""

import base64
import threading
import cv2
import requests

from config import OLLAMA_URL, OLLAMA_MODEL, MAX_SUMMARY_TOKENS


class SceneSummariser:
    """
    Sends a compressed JPEG frame to a local Ollama vision model
    and stores the one-sentence scene description.

    Runs in a background thread so it never blocks the video loop.
    Only one request is in-flight at a time.
    """

    _PROMPT = (
        "Describe this scene in ONE sentence. "
        "Mention people, objects, and notable activities. Be concise."
    )

    def __init__(self,
                 model: str = OLLAMA_MODEL,
                 url: str   = OLLAMA_URL,
                 max_tokens: int = MAX_SUMMARY_TOKENS):
        self.model      = model
        self.url        = url
        self.max_tokens = max_tokens

        self.last_summary: str = "Waiting for first summary…"
        self._lock    = threading.Lock()
        self._running = False

    # ── public ──────────────────────────────────────────────────────────

    def summarise_async(self, frame) -> None:
        """Fire-and-forget: send frame to Ollama in a daemon thread."""
        with self._lock:
            if self._running:
                return          # previous request still in-flight — skip
            self._running = True

        t = threading.Thread(
            target=self._call,
            args=(frame.copy(),),
            daemon=True,
        )
        t.start()

    @property
    def is_busy(self) -> bool:
        with self._lock:
            return self._running

    # ── private ─────────────────────────────────────────────────────────

    def _call(self, frame) -> None:
        try:
            b64 = self._encode(frame)
            payload = {
                "model":  self.model,
                "prompt": self._PROMPT,
                "images": [b64],
                "stream": False,
                "options": {"num_predict": self.max_tokens},
            }
            r = requests.post(self.url, json=payload, timeout=30)
            if r.ok:
                text = r.json().get("response", "").strip()
                self.last_summary = text or self.last_summary
            else:
                self.last_summary = f"[HTTP {r.status_code}]"
        except requests.exceptions.ConnectionError:
            self.last_summary = "[Ollama not running — start with: ollama serve]"
        except Exception as e:
            self.last_summary = f"[Error: {e}]"
        finally:
            with self._lock:
                self._running = False

    @staticmethod
    def _encode(frame, quality: int = 55) -> str:
        """Compress frame to JPEG and return base64 string."""
        _, buf = cv2.imencode(".jpg", frame,
                              [cv2.IMWRITE_JPEG_QUALITY, quality])
        return base64.b64encode(buf).decode()