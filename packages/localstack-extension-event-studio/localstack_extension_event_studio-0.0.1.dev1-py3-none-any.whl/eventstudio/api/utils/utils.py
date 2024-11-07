import json
import logging
import re
from datetime import datetime
from enum import Enum
from typing import List, Pattern, Type, TypeVar

from localstack.aws.api.events import PutEventsRequestEntry
from localstack.http import Request
from pydantic import BaseModel
from sqlalchemy.types import JSON, TypeDecorator

from eventstudio.api.types.events import EventModel, EventModelList, EventsEventPartialData

LOG = logging.getLogger(__name__)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Enum):
            return obj.value

        # allow us to work with nested models
        if isinstance(obj, EventModel):
            return obj.model_dump()

        if isinstance(obj, EventModelList):
            return obj.model_dump()

        return super().default(obj)


class JSONEncodedDict(TypeDecorator):
    """Represents an immutable structure as a json-encoded string."""

    impl = JSON
    cache_ok = True

    def __init__(self, encoder=None, *args, **kwargs):
        self.encoder = encoder or CustomJSONEncoder
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value, cls=self.encoder)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


def pars_timestamp_ms(timestamp_ms: str) -> datetime:
    timestamp_s = int(timestamp_ms) / 1000
    parsed_time = datetime.fromtimestamp(timestamp_s)

    return parsed_time


def convert_raw_entry(entry: PutEventsRequestEntry) -> EventsEventPartialData:
    """Convert put event request that can also fail validation"""
    return EventsEventPartialData(
        version="0",
        detail_type=entry.get("DetailType"),
        source=entry.get("Source"),
        resources=entry.get("Resources", []),
        detail=json.loads(entry.get("Detail", "{}")),
    )


T = TypeVar("T", bound=BaseModel)


def parse_request_body(request: Request, model: Type[T]) -> T:
    request_data = request.data.decode("utf-8")
    body_dict = json.loads(request_data)
    return model(**body_dict)


def compile_regex_patterns(patterns: List[str]) -> List[Pattern]:
    """Compile a list of regex patterns."""
    return [re.compile(pattern) for pattern in patterns]
