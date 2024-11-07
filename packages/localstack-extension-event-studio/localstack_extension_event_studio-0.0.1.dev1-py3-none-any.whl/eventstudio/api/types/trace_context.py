from pydantic import BaseModel, ConfigDict


class TraceContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    trace_id: str | None = None
    parent_id: str | None = None
    version: int = 0
