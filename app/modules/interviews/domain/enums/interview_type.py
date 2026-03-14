from enum import Enum


class InterviewType(str, Enum):
    SCREENING = "screening"
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    FINAL = "final"
