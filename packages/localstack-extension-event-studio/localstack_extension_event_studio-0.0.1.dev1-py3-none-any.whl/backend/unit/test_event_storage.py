import uuid

import pytest

from eventstudio.api.event_storage import EventStorageService
from eventstudio.api.types.events import InputEventModel
from eventstudio.api.types.services import ServiceName
from tests.backend.sample_data import (
    new_raw_event_events,
    new_raw_event_lambda,
    new_raw_event_s3,
    new_raw_event_sns,
    new_raw_event_sqs,
)


@pytest.fixture
def event_storage() -> EventStorageService:
    return EventStorageService("")


def get_new_event(service: ServiceName) -> InputEventModel:
    case = {
        ServiceName.EVENTS: new_raw_event_events,
        ServiceName.LAMBDA: new_raw_event_lambda,
        ServiceName.SNS: new_raw_event_sns,
        ServiceName.SQS: new_raw_event_sqs,
        ServiceName.S3: new_raw_event_s3,
    }

    new_raw_event = case.get(service)
    if new_raw_event is None:
        raise ValueError(f"Unsupported service type: {service}")

    return InputEventModel(**new_raw_event)


input_event_type = [
    ServiceName.EVENTS,
    ServiceName.LAMBDA,
    ServiceName.SNS,
    ServiceName.SQS,
    ServiceName.S3,
]


@pytest.mark.parametrize("input_event_type", input_event_type)
def test_add_new_item(event_storage, input_event_type):
    input_event = get_new_event(input_event_type)
    spand_id, _ = event_storage.add_event(input_event)

    events_in_db = event_storage.list_events()
    assert len(events_in_db) == 1
    assert events_in_db[0].span_id == spand_id


@pytest.mark.parametrize("input_event_type", input_event_type)
def test_list_items(event_storage, input_event_type):
    # after being added events get expanged, so we need to save the value beforehand
    input_event_one = get_new_event(input_event_type)
    span_id_one, _ = event_storage.add_event(input_event_one)

    input_event_two = get_new_event(input_event_type)
    span_id_two, _ = event_storage.add_event(input_event_two)

    events = event_storage.list_events()
    assert len(events) == 2
    assert events[0].span_id == span_id_one
    assert events[1].span_id == span_id_two


@pytest.mark.parametrize("input_event_type", input_event_type)
def test_delete_item(event_storage, input_event_type):
    input_event = get_new_event(input_event_type)
    span_id, _ = event_storage.add_event(input_event)

    assert len(event_storage.list_events()) == 1

    event_storage.delete_event(span_id)
    assert len(event_storage.list_events()) == 0


def test_get_event_by_id(event_storage: EventStorageService):
    input_event = get_new_event(ServiceName.SQS)
    input_event.event_id = str(uuid.uuid4())
    span_id, _ = event_storage.add_event(input_event)

    event = event_storage.get_event_by_id(input_event.event_id)
    assert event.span_id == span_id
