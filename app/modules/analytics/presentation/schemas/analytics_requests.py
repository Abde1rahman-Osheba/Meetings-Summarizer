from pydantic import BaseModel


class BaseRequest(BaseModel):
    trace_id: str | None = None
