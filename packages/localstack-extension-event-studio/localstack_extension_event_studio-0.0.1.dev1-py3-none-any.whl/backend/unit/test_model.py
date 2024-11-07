import pytest

from eventstudio.api.types.events import EventModelList, InputEventModelList
from tests.backend.sample_data import (
    new_database_event_events,
    new_database_event_lambda,
    new_database_event_s3,
    new_database_event_sns,
    new_database_event_sqs,
    new_raw_event_events,
    new_raw_event_lambda,
    new_raw_event_s3,
    new_raw_event_sns,
    new_raw_event_sqs,
)


@pytest.mark.parametrize(
    "raw_input_event",
    [
        new_raw_event_events,
        new_raw_event_lambda,
        new_raw_event_sns,
        new_raw_event_sqs,
        new_raw_event_s3,
    ],
)
def test_events_to_input_model(raw_input_event):
    events = InputEventModelList(events=[raw_input_event])
    assert events


@pytest.mark.parametrize(
    "database_event",
    [
        new_database_event_events,
        new_database_event_lambda,
        new_database_event_sns,
        new_database_event_sqs,
        new_database_event_s3,
    ],
)
def test_events_to_database_model(database_event):
    events = EventModelList(events=[database_event])
    assert events
