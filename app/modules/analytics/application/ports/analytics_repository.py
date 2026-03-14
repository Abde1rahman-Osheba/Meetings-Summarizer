from typing import Protocol, Any


class AnalyticsRepository(Protocol):
    def get_by_id(self, entity_id: str) -> dict[str, Any] | None: ...
