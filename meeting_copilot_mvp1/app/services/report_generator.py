"""Generate Markdown/JSON/PDF meeting outputs."""

from __future__ import annotations

import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

from app.config import settings
from app.schemas import FinalReportPayload


class ReportGenerator:
    """Create final deliverables from meeting payload."""

    def __init__(self, export_dir: Path | None = None) -> None:
        self.export_dir = export_dir or settings.export_dir
        self.export_dir.mkdir(parents=True, exist_ok=True)

    def export_json(self, session_id: int, payload: FinalReportPayload) -> Path:
        path = self.export_dir / f"session_{session_id}_summary.json"
        path.write_text(json.dumps(payload.model_dump(), indent=2), encoding="utf-8")
        return path

    def export_markdown(self, session_id: int, payload: FinalReportPayload, transcript_markdown: str) -> Path:
        path = self.export_dir / f"session_{session_id}_report.md"
        sections = [
            f"# {payload.meeting_title}",
            f"- Date/Time: {payload.date_time}",
            f"- Duration: {payload.duration}",
            "\n## Executive Summary\n" + payload.executive_summary,
            "\n## Key Topics\n" + "\n".join(f"- {item}" for item in payload.key_topics),
            "\n## Decisions\n" + "\n".join(f"- {item}" for item in payload.decisions),
            "\n## Action Items\n"
            + "\n".join(
                f"- {item.description} (owner: {item.owner}, due: {item.due_date}, status: {item.status})"
                for item in payload.action_items
            ),
            "\n## Blockers / Risks\n" + "\n".join(f"- {item}" for item in payload.blockers_risks),
            "\n## Open Questions\n" + "\n".join(f"- {item}" for item in payload.open_questions),
            "\n## Chronological Highlights\n" + "\n".join(f"- {item}" for item in payload.chronological_highlights),
            "\n## Transcript Appendix\n" + transcript_markdown,
        ]
        path.write_text("\n".join(sections), encoding="utf-8")
        return path

    def export_pdf(self, session_id: int, payload: FinalReportPayload, transcript_markdown: str) -> Path:
        path = self.export_dir / f"session_{session_id}_report.pdf"
        doc = SimpleDocTemplate(str(path), pagesize=LETTER, title=payload.meeting_title)
        styles = getSampleStyleSheet()
        cover_style = ParagraphStyle("Cover", parent=styles["Title"], textColor=colors.HexColor("#1f4e79"))
        body = styles["BodyText"]
        heading = styles["Heading2"]

        story = [
            Spacer(1, 80),
            Paragraph(settings.report_brand, cover_style),
            Spacer(1, 20),
            Paragraph(payload.meeting_title, styles["Title"]),
            Spacer(1, 12),
            Paragraph(f"Date/Time: {payload.date_time}", body),
            Paragraph(f"Duration: {payload.duration}", body),
            PageBreak(),
            Paragraph("Executive Summary", heading),
            Paragraph(payload.executive_summary, body),
        ]

        def add_bullets(title: str, items: list[str]) -> None:
            story.append(Spacer(1, 12))
            story.append(Paragraph(title, heading))
            for item in items or ["None recorded"]:
                story.append(Paragraph(f"• {item}", body))

        add_bullets("Key Topics", payload.key_topics)
        add_bullets("Decisions", payload.decisions)
        add_bullets(
            "Action Items",
            [f"{a.description} (owner: {a.owner}, due: {a.due_date}, status: {a.status})" for a in payload.action_items],
        )
        add_bullets("Blockers / Risks", payload.blockers_risks)
        add_bullets("Open Questions", payload.open_questions)
        add_bullets("Chronological Highlights", payload.chronological_highlights)

        story.append(PageBreak())
        story.append(Paragraph("Transcript Appendix", heading))
        for line in transcript_markdown.splitlines():
            story.append(Paragraph(line or " ", body))

        doc.build(story)
        return path
