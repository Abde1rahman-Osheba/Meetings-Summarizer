from typing import Any


class AuthService:
    ROLE_PERMISSIONS: dict[str, set[str]] = {
        "admin": {"users:write", "jobs:write", "organizations:write"},
        "recruiter": {"candidates:read", "jobs:read"},
        "hiring_manager": {"jobs:write", "interviews:write"},
    }

    def __init__(self) -> None:
        self._store: dict[str, Any] = {}

    def execute(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"status": "ok", "payload": payload}

    def can(self, role: str, permission: str) -> bool:
        return permission in self.ROLE_PERMISSIONS.get(role, set())
