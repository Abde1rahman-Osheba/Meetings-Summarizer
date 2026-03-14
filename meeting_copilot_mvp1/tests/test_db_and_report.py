from pathlib import Path

from app.db import create_session, get_db, init_db, list_transcript_chunks, save_transcript_chunk
from app.schemas import ActionItem, FinalReportPayload
from app.services.report_generator import ReportGenerator


def test_transcript_chunk_persistence(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'test.db'}")
    from app import config as config_module

    config_module.settings.database_url = f"sqlite:///{tmp_path / 'test.db'}"
    from app import db as db_module

    db_module.engine = db_module.create_engine(config_module.settings.database_url, future=True)
    db_module.SessionLocal.configure(bind=db_module.engine)
    init_db()

    with get_db() as db:
        session = create_session(db, "My meeting")
        save_transcript_chunk(db, session.id, "Speaker 1", "Hello", 0.0, 2.0, 0.8, True)
        chunks = list_transcript_chunks(db, session.id)
        assert len(chunks) == 1
        assert chunks[0].text == "Hello"


def test_final_report_data_assembly(tmp_path):
    reporter = ReportGenerator(export_dir=tmp_path)
    payload = FinalReportPayload(
        meeting_title="Weekly Sync",
        date_time="2026-01-01T00:00:00Z",
        duration="00:30:00",
        executive_summary="Great session",
        key_topics=["Roadmap"],
        decisions=["Launch beta"],
        action_items=[ActionItem(description="Prepare deck")],
        blockers_risks=["Budget"],
        open_questions=["Need design signoff?"],
        chronological_highlights=["Kickoff", "Decision made"],
    )

    md = reporter.export_markdown(1, payload, "- transcript")
    js = reporter.export_json(1, payload)

    assert Path(md).exists()
    assert Path(js).exists()
