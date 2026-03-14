"""Pydantic schemas and JSON parsers."""

from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel, Field, ValidationError


class ActionItem(BaseModel):
    description: str
    owner: str = "unknown"
    due_date: str = "unknown"
    status: str = "open"


class SummaryPayload(BaseModel):
    rolling_summary: str
    key_discussion_points: list[str] = Field(default_factory=list)
    decisions: list[str] = Field(default_factory=list)
    action_items: list[ActionItem] = Field(default_factory=list)
    blockers_risks: list[str] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)


class FinalReportPayload(BaseModel):
    meeting_title: str
    date_time: str
    duration: str
    executive_summary: str
    key_topics: list[str]
    decisions: list[str]
    action_items: list[ActionItem]
    blockers_risks: list[str]
    open_questions: list[str]
    chronological_highlights: list[str]


def parse_json_payload(text: str) -> dict[str, Any]:
    """Parse raw JSON string and raise ValueError when invalid."""

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc}") from exc


def parse_summary_payload(text: str) -> SummaryPayload:
    """Validate LLM summary output."""

    payload = parse_json_payload(text)
    try:
        return SummaryPayload.model_validate(payload)
    except ValidationError as exc:
        raise ValueError(f"Invalid summary payload: {exc}") from exc


def parse_final_report_payload(text: str) -> FinalReportPayload:
    """Validate LLM final report output."""

    payload = parse_json_payload(text)
    try:
        return FinalReportPayload.model_validate(payload)
    except ValidationError as exc:
        raise ValueError(f"Invalid final report payload: {exc}") from exc
