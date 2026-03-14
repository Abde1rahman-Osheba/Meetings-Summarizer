from enum import Enum


class CandidateStatus(str, Enum):
    NEW = "new"
    SCREENING = "screening"
    INTERVIEWING = "interviewing"
    HIRED = "hired"
    REJECTED = "rejected"
