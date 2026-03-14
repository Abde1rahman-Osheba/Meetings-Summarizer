"""Meeting state aggregation logic."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.schemas import SummaryPayload


@dataclass
class MeetingState:
    meeting_title: str
    rolling_summary: str = ""
    key_discussion_points: list[str] = field(default_factory=list)
    decisions: list[str] = field(default_factory=list)
    action_items: list[dict] = field(default_factory=list)
    blockers_risks: list[str] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)

    def update_from_summary(self, payload: SummaryPayload) -> None:
        self.rolling_summary = payload.rolling_summary
        self.key_discussion_points = _merge_unique(self.key_discussion_points, payload.key_discussion_points)
        self.decisions = _merge_unique(self.decisions, payload.decisions)
        self.action_items = _merge_action_items(self.action_items, [item.model_dump() for item in payload.action_items])
        self.blockers_risks = _merge_unique(self.blockers_risks, payload.blockers_risks)
        self.open_questions = _merge_unique(self.open_questions, payload.open_questions)

    def to_dict(self) -> dict:
        return {
            "meeting_title": self.meeting_title,
            "rolling_summary": self.rolling_summary,
            "key_discussion_points": self.key_discussion_points,
            "decisions": self.decisions,
            "action_items": self.action_items,
            "blockers_risks": self.blockers_risks,
            "open_questions": self.open_questions,
        }


def _merge_unique(existing: list[str], incoming: list[str]) -> list[str]:
    seen = {item.strip().lower() for item in existing}
    result = list(existing)
    for item in incoming:
        key = item.strip().lower()
        if item and key not in seen:
            result.append(item)
            seen.add(key)
    return result


def _merge_action_items(existing: list[dict], incoming: list[dict]) -> list[dict]:
    seen = {item.get("description", "").strip().lower() for item in existing}
    result = list(existing)
    for item in incoming:
        desc = item.get("description", "").strip().lower()
        if desc and desc not in seen:
            result.append(item)
            seen.add(desc)
    return result
