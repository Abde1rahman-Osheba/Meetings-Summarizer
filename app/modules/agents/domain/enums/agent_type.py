from enum import Enum


class AgentType(str, Enum):
    SOURCING_AGENT = "sourcing_agent"
    RANKING_ASSISTANT = "ranking_assistant"
    INTERVIEW_COPILOT = "interview_copilot"
    RECRUITER_ASSISTANT = "recruiter_assistant"
