from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TokenPayload:
    value: str
