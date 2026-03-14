from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ScoreBreakdown:
    value: str
