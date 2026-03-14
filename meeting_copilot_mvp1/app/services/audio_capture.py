"""Audio capture service with Windows-first loopback strategy."""

from __future__ import annotations

import queue
import threading
import time
from dataclasses import dataclass

import numpy as np

from app.utils.logging_utils import get_logger

logger = get_logger(__name__)

try:
    import soundcard as sc
except ImportError:  # pragma: no cover - handled at runtime
    sc = None


@dataclass
class AudioChunk:
    data: np.ndarray
    sample_rate: int
    started_at: float
    ended_at: float
    source: str


class AudioCaptureService:
    """Captures loopback and optional mic audio into chunk queue."""

    def __init__(self, chunk_seconds: int = 5, sample_rate: int = 16_000) -> None:
        self.chunk_seconds = chunk_seconds
        self.sample_rate = sample_rate
        self._running = False
        self._thread: threading.Thread | None = None
        self._queue: queue.Queue[AudioChunk] = queue.Queue(maxsize=128)
        self.status_message = "inactive"
        self.mic_enabled = False

    def start(self, include_mic: bool = False) -> None:
        if self._running:
            return
        self.mic_enabled = include_mic
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        self.status_message = "active"

    def stop(self) -> None:
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2)
        self.status_message = "inactive"

    def read_chunk(self, timeout: float = 0.2) -> AudioChunk | None:
        try:
            return self._queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def _loop(self) -> None:
        if sc is None:
            self.status_message = "soundcard missing; cannot capture"
            logger.error("soundcard library not installed")
            self._running = False
            return

        loopback = sc.default_speaker()
        if not loopback:
            self.status_message = "no loopback speaker device"
            self._running = False
            return

        mic = sc.default_microphone() if self.mic_enabled else None
        if self.mic_enabled and mic is None:
            logger.warning("microphone requested but unavailable")
            self.status_message = "mic unavailable, capturing system audio only"

        frames = self.sample_rate * self.chunk_seconds
        start_ref = time.monotonic()
        try:
            with loopback.recorder(samplerate=self.sample_rate) as loopback_rec:
                mic_rec = mic.recorder(samplerate=self.sample_rate) if mic else None
                with mic_rec if mic_rec else _NullContextManager():
                    while self._running:
                        chunk_start = time.monotonic() - start_ref
                        sys_audio = loopback_rec.record(numframes=frames)
                        mix = np.mean(sys_audio, axis=1) if sys_audio.ndim > 1 else sys_audio

                        source = "system"
                        if mic_rec:
                            mic_audio = mic_rec.record(numframes=frames)
                            mic_mono = np.mean(mic_audio, axis=1) if mic_audio.ndim > 1 else mic_audio
                            mix = np.clip((mix + mic_mono) / 2.0, -1.0, 1.0)
                            source = "system+mic"

                        chunk_end = time.monotonic() - start_ref
                        audio_chunk = AudioChunk(
                            data=mix.astype(np.float32),
                            sample_rate=self.sample_rate,
                            started_at=chunk_start,
                            ended_at=chunk_end,
                            source=source,
                        )
                        if not self._queue.full():
                            self._queue.put(audio_chunk)
        except Exception as exc:  # pragma: no cover - hardware dependent
            logger.error("Audio capture loop failed: %s", exc)
            self.status_message = f"audio capture error: {exc}"
            self._running = False


class _NullContextManager:
    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc, tb):
        return False
