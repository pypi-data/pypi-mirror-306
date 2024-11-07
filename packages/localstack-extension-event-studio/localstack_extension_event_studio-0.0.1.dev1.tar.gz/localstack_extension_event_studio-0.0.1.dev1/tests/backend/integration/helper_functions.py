import pytest
import requests
from localstack.utils.sync import retry
from requests.exceptions import RequestException

from eventstudio.api.config import Config
from eventstudio.api.types.events import EventModelList, InputEventModelList
from eventstudio.api.types.responses import (
    AddEventsResponse,
    DeleteEventsResponse,
    ReplayEventsResponse,
)


def add_events(events: InputEventModelList) -> AddEventsResponse:
    try:
        response = requests.post(
            Config.get_full_url(Config.EVENTS), json={"events": events}, timeout=5
        )
        response.raise_for_status()
        return response
    except RequestException as e:
        pytest.fail(f"Failed to add events: {str(e)}")


def add_single_event(event: dict) -> AddEventsResponse:
    add_events_response = add_events([event])
    assert add_events_response.status_code == 200
    assert add_events_response.json()["FailedEntryCount"] == 0
    return add_events_response


def list_events() -> EventModelList:
    try:
        response = requests.get(Config.get_full_url(Config.EVENTS), timeout=5)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        pytest.fail(f"Failed to fetch events: {str(e)}")
    except ValueError as e:
        pytest.fail(f"Failed to parse JSON response: {str(e)}")


def list_event_details(span_id: str) -> EventModelList:
    try:
        response = requests.get(Config.get_full_url(Config.EVENTS) + f"/{span_id}", timeout=5)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        pytest.fail(f"Failed to fetch event details: {str(e)}")
    except ValueError as e:
        pytest.fail(f"Failed to parse JSON response: {str(e)}")


def delete_events(span_ids: list[str]) -> DeleteEventsResponse:
    try:
        response = requests.delete(
            Config.get_full_url(Config.EVENTS), json={"span_ids": span_ids}, timeout=5
        )
        response.raise_for_status()
        return response
    except RequestException as e:
        pytest.fail(f"Failed to delete events: {str(e)}")


def delete_all_events():
    try:
        response = requests.delete(Config.get_full_url(Config.ALL_EVENTS), timeout=5)
        response.raise_for_status()
        return response
    except RequestException as e:
        pytest.fail(f"Failed to delete all events: {str(e)}")


def replay_events(events: EventModelList) -> ReplayEventsResponse:
    try:
        response = requests.post(Config.get_full_url(Config.REPLAY), json=events)  # , timeout=5)
        response.raise_for_status()
        return response
    except RequestException as e:
        pytest.fail(f"Failed to replay events: {str(e)}")


def get_trace_graph(trace_id: str) -> EventModelList:
    try:
        response = requests.get(Config.get_full_url(Config.TRACES) + f"/{trace_id}", timeout=5)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        pytest.fail(f"Failed to fetch trace graph: {str(e)}")
    except ValueError as e:
        pytest.fail(f"Failed to parse JSON response: {str(e)}")


def assert_list_events_len(expected_len: int, retries=3, sleep=1):
    def _assert_list_events_len():
        list_events_response = list_events()
        assert len(list_events_response["events"]) == expected_len
        return list_events_response

    list_events_response = retry(_assert_list_events_len, retries, sleep)
    return list_events_response
