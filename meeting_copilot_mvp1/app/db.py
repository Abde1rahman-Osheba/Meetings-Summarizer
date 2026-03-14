"""Database session and repository helpers."""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings
from app.models import Base, FinalReport, RollingSummary, SessionRecord, TranscriptChunk
from app.utils.time_utils import utc_now


def _resolve_sqlite_path() -> str:
    if settings.database_url.startswith("sqlite:///"):
        path = settings.database_url.removeprefix("sqlite:///")
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    return settings.database_url


engine = create_engine(_resolve_sqlite_path(), future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def init_db() -> None:
    """Create database tables if they do not exist."""

    Base.metadata.create_all(bind=engine)


@contextmanager
def get_db() -> Iterator[Session]:
    """Provide transactional scope for DB operations."""

    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def create_session(db: Session, title: str) -> SessionRecord:
    record = SessionRecord(title=title or "Untitled Meeting", started_at=utc_now(), status="running")
    db.add(record)
    db.flush()
    return record


def end_session(db: Session, session_id: int) -> SessionRecord | None:
    record = db.get(SessionRecord, session_id)
    if not record:
        return None
    record.ended_at = utc_now()
    record.status = "stopped"
    db.flush()
    return record


def save_transcript_chunk(
    db: Session,
    session_id: int,
    speaker_label: str,
    text: str,
    started_at_seconds: float,
    ended_at_seconds: float,
    confidence: float | None,
    estimated_speaker: bool = True,
    language: str = "unknown",
) -> TranscriptChunk:
    chunk = TranscriptChunk(
        session_id=session_id,
        speaker_label=speaker_label,
        language=language,
        text=text,
        started_at_seconds=started_at_seconds,
        ended_at_seconds=ended_at_seconds,
        confidence=confidence,
        created_at=utc_now(),
        estimated_speaker=estimated_speaker,
    )
    db.add(chunk)
    db.flush()
    return chunk


def list_transcript_chunks(db: Session, session_id: int) -> list[TranscriptChunk]:
    stmt = select(TranscriptChunk).where(TranscriptChunk.session_id == session_id).order_by(TranscriptChunk.id.asc())
    return list(db.scalars(stmt))


def save_summary(db: Session, session_id: int, summary_json: dict) -> RollingSummary:
    summary = RollingSummary(session_id=session_id, summary_json=summary_json, created_at=utc_now())
    db.add(summary)
    db.flush()
    return summary


def list_summaries(db: Session, session_id: int) -> list[RollingSummary]:
    stmt = select(RollingSummary).where(RollingSummary.session_id == session_id).order_by(RollingSummary.id.asc())
    return list(db.scalars(stmt))


def save_final_report(
    db: Session,
    session_id: int,
    report_json: dict,
    markdown_path: str | None,
    pdf_path: str | None,
) -> FinalReport:
    existing = db.scalar(select(FinalReport).where(FinalReport.session_id == session_id))
    if existing:
        existing.report_json = report_json
        existing.markdown_path = markdown_path
        existing.pdf_path = pdf_path
        existing.created_at = utc_now()
        db.flush()
        return existing

    record = FinalReport(
        session_id=session_id,
        report_json=report_json,
        markdown_path=markdown_path,
        pdf_path=pdf_path,
        created_at=utc_now(),
    )
    db.add(record)
    db.flush()
    return record
