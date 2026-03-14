"""Core orchestration for session lifecycle."""

from __future__ import annotations

import json
import threading
import time
from dataclasses import dataclass

from app.config import settings
from app.db import (
    create_session,
    end_session,
    get_db,
    init_db,
    list_transcript_chunks,
    save_final_report,
    save_summary,
    save_transcript_chunk,
)
from app.schemas import FinalReportPayload, SummaryPayload
from app.services.audio_capture import AudioCaptureService
from app.services.ollama_client import OllamaClient
from app.services.report_generator import ReportGenerator
from app.services.state_manager import MeetingState
from app.services.summarization import SummarizationService
from app.services.transcription import TranscriptionService
from app.utils.logging_utils import get_logger
from app.utils.time_utils import format_duration

logger = get_logger(__name__)


@dataclass
class RuntimeStatus:
    ollama_connected: bool = False
    audio_capture_active: bool = False
    transcription_active: bool = False
    last_error: str = ""


class MeetingCopilotApp:
    """Orchestrates audio capture, transcription, summaries, and exports."""

    def __init__(self) -> None:
        init_db()
        self.audio = AudioCaptureService(chunk_seconds=settings.chunk_seconds)
        self.transcriber = TranscriptionService()
        self.ollama = OllamaClient()
        self.summarizer = SummarizationService()
        self.reporter = ReportGenerator()

        self.status = RuntimeStatus()
        self.session_id: int | None = None
        self.state: MeetingState | None = None
        self._running = False
        self._worker_thread: threading.Thread | None = None
        self._last_summary_ts = 0.0

    def check_dependencies(self) -> RuntimeStatus:
        self.status.ollama_connected = self.ollama.health_check()
        self.transcriber.initialize()
        self.status.transcription_active = self.transcriber.model is not None
        return self.status

    def start_session(self, title: str, include_mic: bool = False) -> int:
        with get_db() as db:
            session = create_session(db, title)
            self.session_id = session.id

        self.state = MeetingState(meeting_title=title or "Untitled Meeting")
        self._running = True
        self._last_summary_ts = time.monotonic()
        self.audio.start(include_mic=include_mic)
        self.status.audio_capture_active = True

        self._worker_thread = threading.Thread(target=self._processing_loop, daemon=True)
        self._worker_thread.start()
        return self.session_id

    def stop_session(self) -> None:
        self._running = False
        self.audio.stop()
        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=3)
        self.status.audio_capture_active = False

        if self.session_id is not None:
            with get_db() as db:
                end_session(db, self.session_id)

    def summarize_now(self) -> SummaryPayload | None:
        if self.session_id is None or self.state is None:
            return None
        with get_db() as db:
            chunks = list_transcript_chunks(db, self.session_id)
        transcript_context = _chunks_to_context(chunks[-20:])
        payload = self.summarizer.build_rolling_summary(transcript_context, self.state.to_dict())
        self.state.update_from_summary(payload)
        with get_db() as db:
            save_summary(db, self.session_id, payload.model_dump())
        return payload

    def _processing_loop(self) -> None:
        while self._running and self.session_id is not None and self.state is not None:
            chunk = self.audio.read_chunk(timeout=0.3)
            if chunk is None:
                self._maybe_rolling_summary()
                continue

            segments = self.transcriber.transcribe_chunk(chunk)
            if not segments:
                self._maybe_rolling_summary()
                continue

            with get_db() as db:
                for seg in segments:
                    save_transcript_chunk(
                        db,
                        session_id=self.session_id,
                        speaker_label=seg["speaker_label"],
                        text=seg["text"],
                        started_at_seconds=seg["start"],
                        ended_at_seconds=seg["end"],
                        confidence=seg["confidence"],
                        estimated_speaker=seg.get("estimated_speaker", True),
                        language=seg.get("language", "unknown"),
                    )

            self._maybe_rolling_summary()

    def _maybe_rolling_summary(self) -> None:
        now = time.monotonic()
        if now - self._last_summary_ts < settings.summary_interval_seconds:
            return
        try:
            self.summarize_now()
        except Exception as exc:  # pragma: no cover
            logger.error("rolling summary failed: %s", exc)
            self.status.last_error = f"Rolling summary failed: {exc}"
        finally:
            self._last_summary_ts = now

    def build_final_outputs(self) -> dict[str, str]:
        if self.session_id is None or self.state is None:
            raise RuntimeError("No active session data")

        with get_db() as db:
            session = end_session(db, self.session_id)
            chunks = list_transcript_chunks(db, self.session_id)

        transcript_md = _transcript_markdown(chunks)
        if session and session.ended_at:
            duration = format_duration(session.started_at, session.ended_at)
            date_time = session.started_at.isoformat()
        else:
            duration = "unknown"
            date_time = "unknown"

        aggregate = self.state.to_dict() | {"duration": duration, "date_time": date_time}
        payload: FinalReportPayload = self.summarizer.build_final_report(transcript_md, aggregate)

        json_path = self.reporter.export_json(self.session_id, payload)
        md_path = self.reporter.export_markdown(self.session_id, payload, transcript_md)
        pdf_path = self.reporter.export_pdf(self.session_id, payload, transcript_md)

        with get_db() as db:
            save_final_report(
                db,
                session_id=self.session_id,
                report_json=json.loads(payload.model_dump_json()),
                markdown_path=str(md_path),
                pdf_path=str(pdf_path),
            )

        return {
            "json": str(json_path),
            "markdown": str(md_path),
            "pdf": str(pdf_path),
        }


def _chunks_to_context(chunks: list) -> str:
    return "\n".join(
        f"[{chunk.started_at_seconds:.1f}-{chunk.ended_at_seconds:.1f}] {chunk.speaker_label}: {chunk.text}" for chunk in chunks
    )


def _transcript_markdown(chunks: list) -> str:
    return "\n".join(
        f"- ({chunk.started_at_seconds:.1f}s - {chunk.ended_at_seconds:.1f}s) **{chunk.speaker_label}**: {chunk.text}"
        for chunk in chunks
    )
