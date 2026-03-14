"""Streamlit UI for Meeting Copilot MVP1."""

from __future__ import annotations

import json
import time
from pathlib import Path

import streamlit as st

from app.db import get_db, list_summaries, list_transcript_chunks
from app.main import MeetingCopilotApp

st.set_page_config(page_title="Meeting Copilot MVP1", layout="wide")

if "copilot" not in st.session_state:
    st.session_state.copilot = MeetingCopilotApp()
if "session_id" not in st.session_state:
    st.session_state.session_id = None

copilot: MeetingCopilotApp = st.session_state.copilot

st.title("Meeting Copilot MVP1 (Local-First)")

with st.sidebar:
    st.header("Session Controls")
    title = st.text_input("Meeting Title", value="Weekly Sync")
    include_mic = st.checkbox("Include microphone (optional)", value=False)

    if st.button("Check Dependencies"):
        status = copilot.check_dependencies()
        st.success(f"Ollama: {'connected' if status.ollama_connected else 'disconnected'}")
        st.info(f"Transcription: {'active' if status.transcription_active else 'inactive'}")

    col1, col2 = st.columns(2)
    if col1.button("Start Meeting Session", use_container_width=True):
        sid = copilot.start_session(title=title, include_mic=include_mic)
        st.session_state.session_id = sid
        st.success(f"Session started: {sid}")

    if col2.button("Stop Meeting Session", use_container_width=True):
        copilot.stop_session()
        st.warning("Session stopped")

    if st.button("Summarize Now"):
        payload = copilot.summarize_now()
        if payload:
            st.success("Summary updated")
        else:
            st.warning("No active session")

    if st.button("Export PDF / Markdown / JSON"):
        try:
            paths = copilot.build_final_outputs()
            st.success("Exports complete")
            for key, path in paths.items():
                st.write(f"{key.upper()}: `{path}`")
        except Exception as exc:
            st.error(f"Export failed: {exc}")

    st.divider()
    st.subheader("Status")
    st.write(f"Ollama: {'🟢' if copilot.status.ollama_connected else '🔴'}")
    st.write(f"Audio capture: {'🟢' if copilot.status.audio_capture_active else '🔴'}")
    st.write(f"Transcription: {'🟢' if copilot.status.transcription_active else '🔴'}")
    if copilot.audio.status_message:
        st.caption(f"Audio detail: {copilot.audio.status_message}")
    if copilot.status.last_error:
        st.error(copilot.status.last_error)

if st.session_state.session_id:
    sid = st.session_state.session_id
    with get_db() as db:
        chunks = list_transcript_chunks(db, sid)
        summaries = list_summaries(db, sid)

    left, right = st.columns(2)

    with left:
        st.subheader("Live Transcript")
        transcript_lines = [
            f"[{c.started_at_seconds:.1f}-{c.ended_at_seconds:.1f}] {c.speaker_label} [{c.language}] ({'estimated' if c.estimated_speaker else 'direct'}): {c.text}"
            for c in chunks[-150:]
        ]
        st.text_area("Transcript", value="\n".join(transcript_lines), height=420)

    with right:
        st.subheader("Live Summary")
        latest_summary = summaries[-1].summary_json if summaries else {}
        st.text_area("Rolling Summary", value=latest_summary.get("rolling_summary", "No summary yet"), height=120)

        st.subheader("Decisions")
        for item in latest_summary.get("decisions", []):
            st.markdown(f"- {item}")

        st.subheader("Action Items")
        for item in latest_summary.get("action_items", []):
            st.markdown(
                f"- {item.get('description', '')} (owner: {item.get('owner', 'unknown')}, due: {item.get('due_date', 'unknown')})"
            )

        st.subheader("Open Questions")
        for item in latest_summary.get("open_questions", []):
            st.markdown(f"- {item}")

    if st.button("Refresh"):
        time.sleep(0.1)
        st.rerun()
else:
    st.info("Start a meeting session to view live transcript and summaries.")
