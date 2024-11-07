from tests.backend.integration.helper_functions import (
    assert_list_events_len,
    get_trace_graph,
)
from tests.backend.sample_data import (
    EVENT_NO_EVENT_BUS_NAME,
)


def test_list_events_from_test_stack(
    event_bridge_infra,
    stack_name,
    aws_client,
    cleanup_events_in_db,
    snapshot_with_default_transformers,
    snapshot,
):
    cleanup_events_in_db()

    outputs = event_bridge_infra.get_stack_outputs(stack_name)
    event_bus_name = outputs["EventBusName"]
    lambda_function_name = outputs["LambdaFunctionName"]

    entries = [{**EVENT_NO_EVENT_BUS_NAME, "EventBusName": event_bus_name}]
    response = aws_client.events.put_events(Entries=entries)
    assert response["FailedEntryCount"] == 0

    # Query the extension list_events endpoint to check if the event was received
    extension_events = assert_list_events_len(32, retries=15, sleep=2)
    snapshot_with_default_transformers.add_transformers_list(
        [snapshot.transform.regex(lambda_function_name, "test-function-name")],
    )
    snapshot.match("list_event_response", extension_events)


def test_trace_graph_from_test_stack(
    event_bridge_infra,
    stack_name,
    aws_client,
    cleanup_events_in_db,
    snapshot_with_default_transformers,
    snapshot,
):
    cleanup_events_in_db()

    outputs = event_bridge_infra.get_stack_outputs(stack_name)
    event_bus_name = outputs["EventBusName"]
    lambda_function_name = outputs["LambdaFunctionName"]

    entries = [{**EVENT_NO_EVENT_BUS_NAME, "EventBusName": event_bus_name}]
    response = aws_client.events.put_events(Entries=entries)
    assert response["FailedEntryCount"] == 0

    # Get the trace graph
    extension_events = assert_list_events_len(32, retries=15, sleep=2)
    trace_id = extension_events["events"][0]["trace_id"]
    trace_graph = get_trace_graph(trace_id)
    snapshot_with_default_transformers.add_transformers_list(
        [snapshot.transform.regex(lambda_function_name, "test-function-name")],
    )
    snapshot.match("trace_graph", trace_graph)
