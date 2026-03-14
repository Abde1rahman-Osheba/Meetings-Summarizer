from typing import Any


class UserService:
    def __init__(self) -> None:
        self._store: dict[str, Any] = {}

    def execute(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"status": "ok", "payload": payload}

