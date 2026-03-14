"""Live and final summarization via Ollama."""

from __future__ import annotations

from pathlib import Path

from app.schemas import FinalReportPayload, SummaryPayload, parse_final_report_payload, parse_summary_payload
from app.services.ollama_client import OllamaClient
from app.utils.logging_utils import get_logger

logger = get_logger(__name__)


class SummarizationService:
    """Creates rolling summaries and final report payloads."""

    def __init__(self, prompt_dir: Path | None = None, ollama_client: OllamaClient | None = None) -> None:
        self.prompt_dir = prompt_dir or Path("app/prompts")
        self.ollama_client = ollama_client or OllamaClient()
        self.live_prompt = (self.prompt_dir / "live_summary.txt").read_text(encoding="utf-8")
        self.final_prompt = (self.prompt_dir / "final_report.txt").read_text(encoding="utf-8")

    def build_rolling_summary(self, transcript_context: str, current_state: dict) -> SummaryPayload:
        prompt = self.live_prompt.format(transcript_context=transcript_context, current_state=current_state)
        response = self.ollama_client.generate_json(prompt=prompt)
        try:
            return parse_summary_payload(response)
        except ValueError:
            logger.warning("Invalid rolling summary JSON; using fallback payload")
            return SummaryPayload(rolling_summary="No reliable summary for this window.")

    def build_final_report(self, transcript_markdown: str, aggregate_state: dict) -> FinalReportPayload:
        prompt = self.final_prompt.format(transcript_markdown=transcript_markdown, aggregate_state=aggregate_state)
        response = self.ollama_client.generate_json(prompt=prompt)
        try:
            return parse_final_report_payload(response)
        except ValueError:
            logger.warning("Invalid final report JSON; using fallback payload")
            return FinalReportPayload(
                meeting_title=aggregate_state.get("meeting_title", "Untitled Meeting"),
                date_time=aggregate_state.get("date_time", "unknown"),
                duration=aggregate_state.get("duration", "unknown"),
                executive_summary="Summary unavailable due to parsing error.",
                key_topics=[],
                decisions=aggregate_state.get("decisions", []),
                action_items=aggregate_state.get("action_items", []),
                blockers_risks=aggregate_state.get("blockers_risks", []),
                open_questions=aggregate_state.get("open_questions", []),
                chronological_highlights=[],
            )
