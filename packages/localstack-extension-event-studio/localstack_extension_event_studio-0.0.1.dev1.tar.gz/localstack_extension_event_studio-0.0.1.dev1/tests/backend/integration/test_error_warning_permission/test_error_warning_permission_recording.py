import json

from localstack.utils.strings import short_uid
from tests.backend.integration.helper_functions import (
    assert_list_events_len,
)
from tests.backend.sample_data import (
    EVENT_NO_EVENT_BUS_NAME,
)


class TestEventBridgeWarningRecording:
    def test_event_bridge_not_existing_event_bus_warning(
        self,
        aws_client,
        snapshot,
    ):
        # put event
        entries = [{**EVENT_NO_EVENT_BUS_NAME, "EventBusName": "not-existing-event-bus"}]
        response = aws_client.events.put_events(Entries=entries)
        assert response["FailedEntryCount"] == 0

        list_events_response = assert_list_events_len(1)
        snapshot.match("list_event_response", list_events_response)

    def test_event_bridge_no_rule_warning(
        self,
        events_create_event_bus,
        aws_client,
        snapshot_with_default_transformers,
        snapshot,
    ):
        # create event bus with no rule and no target
        event_bus_name = f"test-event-bus-{short_uid()}"
        events_create_event_bus(Name=event_bus_name)

        # put event
        entries = [{**EVENT_NO_EVENT_BUS_NAME, "EventBusName": event_bus_name}]
        response = aws_client.events.put_events(Entries=entries)
        assert response["FailedEntryCount"] == 0

        list_events_response = assert_list_events_len(2)
        snapshot_with_default_transformers.add_transformers_list(
            [
                snapshot.transform.regex(event_bus_name, "test-event-bus-name"),
            ],
        )
        snapshot.match("list_event_response", list_events_response)

    def test_event_bridge_no_target_warning(
        self,
        events_create_event_bus,
        events_put_rule,
        aws_client,
        snapshot_with_default_transformers,
        snapshot,
    ):
        # create event bus
        event_bus_name = f"test-event-bus-{short_uid()}"
        events_create_event_bus(Name=event_bus_name)

        # create rule
        rule_name = f"test-rule-{short_uid()}"
        events_put_rule(
            Name=rule_name,
            EventPattern=json.dumps({"source": ["core.update-account-command"]}),
            EventBusName=event_bus_name,
        )

        # put event
        entries = [{**EVENT_NO_EVENT_BUS_NAME, "EventBusName": event_bus_name}]
        response = aws_client.events.put_events(Entries=entries)
        assert response["FailedEntryCount"] == 0

        list_events_response = assert_list_events_len(3)
        snapshot_with_default_transformers.add_transformers_list(
            [
                snapshot.transform.regex(event_bus_name, "test-event-bus-name"),
                snapshot.transform.regex(rule_name, "test-rule-name"),
            ],
        )
        snapshot.match("list_event_response", list_events_response)


class TestIAMPermissionRecording:
    def test_iam_logging_handler_callback(
        self,
        events_create_event_bus,
        events_put_rule,
        sqs_create_queue,
        sqs_get_queue_arn,
        aws_client,
        snapshot_with_default_transformers,
        cleanup_events_in_db,
        snapshot,
    ):
        # create event bridge bus
        event_bus_name = f"test-event-bus-{short_uid()}"
        events_create_event_bus(Name=event_bus_name)

        # create queue
        queue_name = f"test-queue-{short_uid()}"
        queue_url = sqs_create_queue(QueueName=queue_name)
        queue_arn = sqs_get_queue_arn(queue_url)

        # create rule
        rule_name = f"test-rule-{short_uid()}"
        response = events_put_rule(
            Name=rule_name,
            EventPattern=json.dumps({"source": ["core.update-account-command"]}),
            EventBusName=event_bus_name,
        )

        target_id = f"test-target-{short_uid()}"
        aws_client.events.put_targets(
            Rule=rule_name,
            EventBusName=event_bus_name,
            Targets=[{"Id": target_id, "Arn": queue_arn}],
        )

        # put event
        entries = [{**EVENT_NO_EVENT_BUS_NAME, "EventBusName": event_bus_name}]
        response = aws_client.events.put_events(Entries=entries)
        assert response["FailedEntryCount"] == 0

        list_events_response = assert_list_events_len(5)
        snapshot_with_default_transformers.add_transformers_list(
            [
                snapshot.transform.regex(queue_name, "test-queue-name"),
                snapshot.transform.regex(event_bus_name, "test-event-bus-name"),
            ],
        )
        snapshot.match("list_event_response", list_events_response)

        cleanup_events_in_db()

    def test_iam_permission_recording_events_sqs(
        self,
        events_create_event_bus,
        events_put_rule,
        sqs_create_queue,
        sqs_get_queue_arn,
        aws_client,
        wait_for_sqs_messages,
        cleanup_events_in_db,
        snapshot_with_default_transformers,
        snapshot,
    ):
        # create event bus
        event_bus_name = f"test-event-bus-{short_uid()}"
        response = events_create_event_bus(Name=event_bus_name)

        # create queue
        queue_name = f"test-queue-{short_uid()}"
        queue_url = sqs_create_queue(QueueName=queue_name)
        queue_arn = sqs_get_queue_arn(queue_url)

        # create rule
        rule_name = f"test-rule-{short_uid()}"
        response = events_put_rule(
            Name=rule_name,
            EventPattern=json.dumps({"source": ["core.update-account-command"]}),
            EventBusName=event_bus_name,
        )

        target_id = f"test-target-{short_uid()}"
        aws_client.events.put_targets(
            Rule=rule_name,
            EventBusName=event_bus_name,
            Targets=[{"Id": target_id, "Arn": queue_arn}],
        )

        # put event
        entries = [{**EVENT_NO_EVENT_BUS_NAME, "EventBusName": event_bus_name}]
        response = aws_client.events.put_events(Entries=entries)
        assert response["FailedEntryCount"] == 0

        wait_for_sqs_messages(queue_url, expected_message_count=1)

        list_events_response = assert_list_events_len(5)
        snapshot_with_default_transformers.add_transformers_list(
            [
                snapshot.transform.regex(queue_name, "test-queue-name"),
                snapshot.transform.regex(event_bus_name, "test-event-bus-name"),
            ],
        )
        snapshot.match("list_event_response", list_events_response)

        assert len(list_events_response["events"][3]["errors"]) == 1

        cleanup_events_in_db()
