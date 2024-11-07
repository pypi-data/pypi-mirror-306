import json

import pytest
from botocore.exceptions import ClientError, ParamValidationError
from localstack.aws.connect import connect_to
from localstack.utils.strings import short_uid
from tests.backend.sample_data import EVENT_NO_EVENT_BUS_NAME


def boto_error_handler(exception, **kwargs):
    if exception is not None:
        print(f"Error: {exception}")


client_factory = connect_to(aws_access_key_id="test", region_name="us-east-1")
client = client_factory.get_client("events")
client.meta.events.register("after-call-error", boto_error_handler)


class TestClientSideValidationErrors:
    def test_put_events_client_side_validation_error(self, event_bridge_infra, stack_name):
        outputs = event_bridge_infra.get_stack_outputs(stack_name)
        event_bus_name = outputs["EventBusName"]

        # test wrong input parameter
        with pytest.raises(ParamValidationError) as e:
            client.put_events(
                Entries=[{**EVENT_NO_EVENT_BUS_NAME, "event-bus-name": event_bus_name}]
            )

        assert "Parameter validation failed" in str(e.value)


class TestServerSideValidationErrors:
    def test_put_events_server_side_validation_error(self, event_bridge_infra, stack_name):
        outputs = event_bridge_infra.get_stack_outputs(stack_name)
        event_bus_name = outputs["EventBusName"]

        # test 11 entries at once
        with pytest.raises(ClientError) as e:
            client.put_events(
                Entries=[
                    {**EVENT_NO_EVENT_BUS_NAME, "EventBusName": event_bus_name} for _ in range(11)
                ]
            )

        assert "ValidationException" in str(e.value)

    @pytest.mark.skip("Bug in EventBridge V2")  # TODO: Fix this
    def test_put_events_server_side_validation_error_appended(self, event_bridge_infra, stack_name):
        outputs = event_bridge_infra.get_stack_outputs(stack_name)
        event_bus_name = outputs["EventBusName"]

        # test missing detail, detail type, source
        response = client.put_events(
            Entries=[
                {
                    **{k: v for k, v in EVENT_NO_EVENT_BUS_NAME.items() if k != "Detail"},
                    "EventBusName": event_bus_name,
                }
            ]
        )
        assert response["FailedEntryCount"] == 1

        response = client.put_events(
            Entries=[
                {
                    **{k: v for k, v in EVENT_NO_EVENT_BUS_NAME.items() if k != "DetailType"},
                    "EventBusName": event_bus_name,
                }
            ]
        )
        assert response["FailedEntryCount"] == 1

        response = client.put_events(
            Entries=[
                {
                    **{k: v for k, v in EVENT_NO_EVENT_BUS_NAME.items() if k != "Source"},
                    "EventBusName": event_bus_name,
                }
            ]
        )
        assert response["FailedEntryCount"] == 1

    def test_put_events_server_side_silent_error(self, event_bridge_infra, stack_name):
        outputs = event_bridge_infra.get_stack_outputs(stack_name)
        print(outputs["EventBusName"])

        # missing event bus currently silently fails #TODO add error handling
        client.put_events(
            Entries=[{**EVENT_NO_EVENT_BUS_NAME, "EventBusName": "this_event_bus_does_not_exist"}]
        )


class TestErrorScenarios:
    def test_events_to_not_existing_sqs(self, events_create_event_bus, events_put_rule):
        event_bus_name = f"test-event-bus-{short_uid()}"
        events_create_event_bus(Name=event_bus_name)

        event_pattern = {
            "source": ["test-source"],
            "detail-type": ["test-detail-type"],
        }

        rule_name = f"test_rule-{short_uid()}"
        events_put_rule(
            Name=rule_name,
            EventBusName=event_bus_name,
            EventPattern=json.dumps(event_pattern),
        )

        target_id = f"target-{short_uid()}"
        client.put_targets(
            Rule=rule_name,
            EventBusName=event_bus_name,
            Targets=[
                {
                    "Id": target_id,
                    "Arn": "arn:aws:sqs:us-east-1:000000000000:this_queue_does_not_exist",
                }
            ],
        )

        response = client.put_events(
            Entries=[
                {
                    "Source": "test-source",
                    "DetailType": "test-detail-type",
                    "Detail": json.dumps({"key": "value"}),
                    "EventBusName": event_bus_name,
                }
            ]
        )

        assert response["FailedEntryCount"] == 1
