from typing import Protocol, Any


class AuditRepository(Protocol):
    def get_by_id(self, entity_id: str) -> dict[str, Any] | None: ...
