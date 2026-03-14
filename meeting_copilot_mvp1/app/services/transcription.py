"""Incremental transcription service using faster-whisper."""

from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

from app.config import settings
from app.services.audio_capture import AudioChunk
from app.utils.logging_utils import get_logger

logger = get_logger(__name__)

try:
    from faster_whisper import WhisperModel
except ImportError:  # pragma: no cover
    WhisperModel = None


class TranscriptionService:
    """Wraps faster-whisper model inference."""

    def __init__(self, model_size: str | None = None, compute_type: str | None = None) -> None:
        self.model_size = model_size or settings.whisper_model_size
        self.compute_type = compute_type or settings.whisper_compute_type
        self.language_priority = _parse_language_priority(settings.whisper_language_priority)
        self.model = None
        self.status_message = "inactive"

    def initialize(self) -> None:
        if WhisperModel is None:
            self.status_message = "faster-whisper not installed"
            return
        self.model = WhisperModel(self.model_size, compute_type=self.compute_type)
        langs = ",".join(self.language_priority)
        self.status_message = f"active (languages: {langs})"

    def transcribe_chunk(self, chunk: AudioChunk) -> list[dict]:
        """Transcribe a single audio chunk into timestamped segments."""

        if self.model is None or chunk.data.size == 0:
            return []

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        try:
            sf.write(tmp_path, np.array(chunk.data), chunk.sample_rate)
            return self._transcribe_with_language_fallback(tmp_path, chunk)
        except Exception as exc:  # pragma: no cover
            logger.error("transcription failed: %s", exc)
            return []
        finally:
            tmp_path.unlink(missing_ok=True)

    def _transcribe_with_language_fallback(self, wav_path: Path, chunk: AudioChunk) -> list[dict]:
        """Try auto detection first, then prioritized language retries."""

        for language in self.language_priority:
            fw_lang = None if language == "auto" else language
            segments, info = self.model.transcribe(
                str(wav_path),
                vad_filter=True,
                task="transcribe",
                language=fw_lang,
            )
            parsed_segments = self._build_segments(list(segments), info, chunk)
            if parsed_segments:
                return parsed_segments
        return []

    def _build_segments(self, segments: list, info: object, chunk: AudioChunk) -> list[dict]:
        transcript_segments: list[dict] = []
        speaker_idx = 1
        detected_language = getattr(info, "language", "unknown") or "unknown"

        for seg in segments:
            text = (seg.text or "").strip()
            if not text:
                continue
            transcript_segments.append(
                {
                    "speaker_label": f"Speaker {speaker_idx}",
                    "estimated_speaker": True,
                    "text": text,
                    "confidence": getattr(seg, "avg_logprob", None),
                    "start": float(seg.start) + chunk.started_at,
                    "end": float(seg.end) + chunk.started_at,
                    "language": detected_language,
                }
            )
            speaker_idx = 1 if speaker_idx == 2 else 2

        return transcript_segments


def _parse_language_priority(raw: str) -> list[str]:
    """Parse language priority string while preserving order and uniqueness."""

    supported = {"auto", "ar", "en"}
    values = [item.strip().lower() for item in raw.split(",") if item.strip()]
    result: list[str] = []
    seen: set[str] = set()

    for value in values:
        if value in supported and value not in seen:
            result.append(value)
            seen.add(value)

    if not result:
        return ["auto", "ar", "en"]
    if "auto" not in seen:
        result.insert(0, "auto")
    return result
