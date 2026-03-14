from enum import Enum


class UserRole(str, Enum):
    RECRUITER = "recruiter"
    HIRING_MANAGER = "hiring_manager"
    ADMIN = "admin"
    INTERVIEWER = "interviewer"
    SYSTEM_OPERATOR = "system_operator"
