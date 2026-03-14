"""SQLAlchemy models for Meeting Copilot MVP1."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for ORM models."""


class SessionRecord(Base):
    """Represents one meeting session."""

    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), default="Untitled Meeting")
    status: Mapped[str] = mapped_column(String(50), default="running")
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)

    transcript_chunks: Mapped[list[TranscriptChunk]] = relationship(back_populates="session")
    summaries: Mapped[list[RollingSummary]] = relationship(back_populates="session")
    report: Mapped[FinalReport | None] = relationship(back_populates="session", uselist=False)


class TranscriptChunk(Base):
    """One transcribed chunk with best-effort labels."""

    __tablename__ = "transcript_chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), index=True)
    speaker_label: Mapped[str] = mapped_column(String(100), default="Unknown Speaker")
    language: Mapped[str] = mapped_column(String(20), default="unknown")
    text: Mapped[str] = mapped_column(Text)
    started_at_seconds: Mapped[float] = mapped_column(Float)
    ended_at_seconds: Mapped[float] = mapped_column(Float)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    estimated_speaker: Mapped[bool] = mapped_column(default=True)

    session: Mapped[SessionRecord] = relationship(back_populates="transcript_chunks")


class RollingSummary(Base):
    """Summary snapshots produced during live session."""

    __tablename__ = "rolling_summaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), index=True)
    summary_json: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    session: Mapped[SessionRecord] = relationship(back_populates="summaries")


class FinalReport(Base):
    """Final assembled meeting report data."""

    __tablename__ = "final_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), unique=True)
    report_json: Mapped[dict] = mapped_column(JSON)
    markdown_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    pdf_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    session: Mapped[SessionRecord] = relationship(back_populates="report")
