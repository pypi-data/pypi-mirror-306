import pytest
from tests.backend.integration.helper_functions import (
    add_events,
    add_single_event,
    delete_all_events,
    delete_events,
    list_event_details,
    list_events,
)
from tests.backend.sample_data import (
    new_raw_event_events,
    new_raw_event_lambda,
    new_raw_event_sns,
    new_raw_event_sqs,
)


@pytest.mark.parametrize(
    "new_raw_event",
    [new_raw_event_events, new_raw_event_lambda, new_raw_event_sns, new_raw_event_sqs],
)
def test_add_list_events_single_event(new_raw_event):
    add_events_response = add_events([new_raw_event])
    assert add_events_response.status_code == 200
    assert add_events_response.json()["FailedEntryCount"] == 0

    # Check if the event was received by backend
    extension_events = list_events()
    assert len(extension_events["events"]) == 1


def test_delete_events_single_event():
    add_single_event(new_raw_event_events)
    list_events_response = list_events()
    span_id = list_events_response["events"][0]["span_id"]

    response = delete_events([span_id])
    assert response.status_code == 200

    extension_events = list_events()
    assert len(extension_events["events"]) == 0


def test_delete_all_events():
    add_single_event(new_raw_event_events)
    add_single_event(new_raw_event_events)
    add_single_event(new_raw_event_events)
    response = list_events()
    assert len(response["events"]) == 3

    response = delete_all_events()
    assert response.status_code == 200

    extension_events = list_events()
    assert len(extension_events["events"]) == 0


@pytest.mark.parametrize(
    "new_raw_event",
    [new_raw_event_events, new_raw_event_lambda, new_raw_event_sns, new_raw_event_sqs],
)
def test_list_event_details(new_raw_event):
    add_single_event(new_raw_event)
    list_events_response = list_events()
    span_id = list_events_response["events"][0]["span_id"]

    response = list_event_details(span_id)
    assert response["event"]["span_id"] == span_id
