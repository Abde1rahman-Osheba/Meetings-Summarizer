from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class RetrievalResult:
    id: str
    data: dict[str, Any] = field(default_factory=dict)
    created_at: datetime | None = None
