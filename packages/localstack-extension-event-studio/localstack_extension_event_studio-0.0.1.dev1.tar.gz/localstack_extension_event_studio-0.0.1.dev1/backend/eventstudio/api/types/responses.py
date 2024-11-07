from typing import Any

from localstack.aws.api.events import Integer, PutEventsResultEntryList
from pydantic import BaseModel
from rolo import Response

from eventstudio.api.types.events import EventModel, EventModelList
from eventstudio.api.utils.utils import CustomJSONEncoder


class Error(BaseModel):
    error: str
    span_id: str | None = None


class FailedEntry(EventModel):
    error: str


class FailedEntryList(BaseModel):
    entries: list[FailedEntry]


class BaseEventsResponse(Response):
    def __init__(
        self,
        status: int,
        response_data: dict[str, Any] | None = None,
        error: str | None = None,
    ):
        super().__init__()
        self.status_code = status
        json_data = {}
        if error:
            json_data["error"] = error
        if response_data:
            json_data.update(response_data)
        if json_data:
            self.set_json(json_data, cls=CustomJSONEncoder)


class AddEventsResponse(BaseEventsResponse):
    def __init__(
        self,
        status: int,
        FailedEntryCount: Integer | None = None,
        FailedEntries: FailedEntryList | None = None,
        error: str | None = None,
    ):
        super().__init__(
            status, {"FailedEntryCount": FailedEntryCount, "FailedEntries": FailedEntries}, error
        )


class DeleteAllEventsResponse(BaseEventsResponse):
    def __init__(self, status: int, error: str | None = None):
        super().__init__(status, error=error)


class DeleteEventsResponse(BaseEventsResponse):
    def __init__(
        self,
        status: int,
        FailedEntryCount: Integer | None = None,
        FailedEntries: FailedEntryList | None = None,
        error: str | None = None,
    ):
        super().__init__(
            status, {"FailedEntryCount": FailedEntryCount, "FailedEntries": FailedEntries}, error
        )


class GetEventResponse(BaseEventsResponse):
    def __init__(self, status: int, event: EventModel | None = None, error: str | None = None):
        super().__init__(status, {"event": event}, error)


class ListEventsResponse(BaseEventsResponse):
    def __init__(self, status: int, events: EventModelList | None = None, error: str | None = None):
        super().__init__(status, {"events": events}, error)


class ReplayEventsResponse(BaseEventsResponse):
    def __init__(
        self,
        status: int,
        FailedEntryCount: Integer | None = None,
        FailedEntries: PutEventsResultEntryList | None = None,
        error: str | None = None,
    ):
        super().__init__(
            status, {"FailedEntryCount": FailedEntryCount, "FailedEntries": FailedEntries}, error
        )


class TraceGraphResponse(BaseEventsResponse):
    def __init__(self, status: int, event: EventModel | None = None, error: str | None = None):
        traces = {event.trace_id: event} if event else {}
        super().__init__(status, {"traces": traces}, error)


class UpdateEventsResponse(BaseEventsResponse):
    def __init__(
        self,
        status: int,
        FailedEntryCount: Integer | None = None,
        FailedEntries: FailedEntryList | None = None,
        error: str | None = None,
    ):
        super().__init__(
            status, {"FailedEntryCount": FailedEntryCount, "FailedEntries": FailedEntries}, error
        )
