from typing import Protocol, Any


class ToolExecutionPort(Protocol):
    def get_by_id(self, entity_id: str) -> dict[str, Any] | None: ...
