import json
import os

import pytest
from localstack.aws.api.lambda_ import Runtime
from localstack.utils.strings import short_uid
from localstack.utils.sync import retry
from tests.backend.integration.helper_functions import (
    assert_list_events_len,
    get_trace_graph,
    replay_events,
)
from tests.backend.sample_data import (
    EVENT_NO_EVENT_BUS_NAME,
    MESSAGE,
)


class TestReplayEvents:
    @pytest.mark.parametrize(
        "event_to_replay",
        [
            {"position": 0, "operation": "raw_input_event", "expected_event_count": 11},
            {"position": 1, "operation": "input_event", "expected_event_count": 11},
        ],
    )
    def test_replay_events_single_event(
        self,
        event_to_replay,
        events_create_event_bus,
        events_put_rule,
        sqs_create_queue,
        sqs_get_queue_arn,
        sqs_allow_events_to_send_messages,
        aws_client,
        wait_for_sqs_messages,
        snapshot_with_default_transformers,
        snapshot,
    ):
        # setup check variables
        position = event_to_replay["position"]
        operation_name = event_to_replay["operation"]
        expected_event_count = event_to_replay["expected_event_count"]

        # create event bus
        event_bus_name = f"test-event-bus-{short_uid()}"
        events_create_event_bus(Name=event_bus_name)

        # create queue
        queue_name = f"test-queue-{short_uid()}"
        queue_url = sqs_create_queue(QueueName=queue_name)
        queue_arn = sqs_get_queue_arn(queue_url)
        sqs_allow_events_to_send_messages(queue_arn, queue_url)

        # create rule
        rule_name = f"test-rule-{short_uid()}"
        events_put_rule(
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

        event_to_replay = list_events_response["events"][position]
        assert event_to_replay["operation_name"] == operation_name
        assert event_to_replay["is_replayable"] is True

        trace_graph_response = get_trace_graph(event_to_replay["trace_id"])
        snapshot.match("trace_graph_response", trace_graph_response)

        replay_events_response = replay_events({"events": [event_to_replay]})
        assert replay_events_response.status_code == 200
        assert replay_events_response.json()["FailedEntryCount"] == 0

        # Check if the event was received by the event bus
        # wait_for_sqs_messages(queue_url, expected_message_count=2, retries=10, sleep=2) # TODO investigate why this is not working in test but manually it works

        list_events_response_after_replay = assert_list_events_len(
            expected_event_count
        )  # +1 since replay operation is also an event that is captured
        snapshot.match("list_event_response_after_replay", list_events_response_after_replay)

        # check update trace graph
        trace_graph_response_after_replay = get_trace_graph(event_to_replay["trace_id"])
        snapshot.match("trace_graph_response_after_replay", trace_graph_response_after_replay)

    def test_replay_lambda_single_event(
        self, aws_client, create_lambda_function, snapshot_with_default_transformers, snapshot
    ):
        # create lambda
        function_name = f"test-function-{short_uid()}"
        create_lambda_function(
            handler_file=os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "lambda_handler.py"
            ),
            func_name=function_name,
            runtime=Runtime.python3_12,
        )

        # invoke lambda
        aws_client.lambda_.invoke(FunctionName=function_name, Payload=json.dumps(MESSAGE))

        list_events_response = assert_list_events_len(1, retries=10, sleep=2)
        event_to_replay = list_events_response["events"][0]
        assert event_to_replay["operation_name"] == "invoke_lambda"
        assert event_to_replay["is_replayable"] is True

        trace_graph_response = get_trace_graph(event_to_replay["trace_id"])
        snapshot_with_default_transformers.add_transformers_list(
            [
                snapshot.transform.regex(function_name, "test-function-name"),
            ]
        )
        snapshot.match("trace_graph_response", trace_graph_response)

        replay_events_response = replay_events({"events": [event_to_replay]})
        assert replay_events_response.status_code == 200

        list_events_response_after_replay = assert_list_events_len(3)
        snapshot.match("list_event_response_after_replay", list_events_response_after_replay)

        # check update trace graph
        trace_graph_response_after_replay = get_trace_graph(event_to_replay["trace_id"])
        snapshot.match("trace_graph_response_after_replay", trace_graph_response_after_replay)

    def test_replay_sqs_single_event(
        self,
        sqs_create_queue,
        aws_client,
        wait_for_sqs_messages,
        snapshot_with_default_transformers,
        snapshot,
    ):
        # create queue
        queue_name = f"test-queue-{short_uid()}"
        queue_url = sqs_create_queue(QueueName=queue_name)

        # send message
        aws_client.sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(MESSAGE))

        wait_for_sqs_messages(queue_url, expected_message_count=1)

        list_events_response = assert_list_events_len(1)
        snapshot_with_default_transformers.add_transformers_list(
            [
                snapshot.transform.regex(queue_name, "test-queue-name"),
            ],
        )
        snapshot.match("list_event_response", list_events_response)

        event_to_replay = list_events_response["events"][0]
        assert event_to_replay["operation_name"] == "send_message"
        assert event_to_replay["is_replayable"] is True

        trace_graph_response = get_trace_graph(event_to_replay["trace_id"])
        snapshot.match("trace_graph_response", trace_graph_response)

        replay_events_response = replay_events({"events": [event_to_replay]})
        assert replay_events_response.status_code == 200

        list_events_response_after_replay = assert_list_events_len(
            3
        )  # +1 since replay operation is also an event that is captured
        snapshot.match("list_event_response_after_replay", list_events_response_after_replay)

        # check update trace graph
        trace_graph_response_after_replay = get_trace_graph(event_to_replay["trace_id"])
        snapshot.match("trace_graph_response_after_replay", trace_graph_response_after_replay)

    def test_replay_sns_single_event(
        self,
        aws_client,
        sqs_create_queue,
        sqs_get_queue_arn,
        sns_create_topic,
        sns_subscription,
        sns_allow_topic_sqs_queue,
        snapshot_with_default_transformers,
        snapshot,
    ):
        # setup sqs queue subscribed to topic
        queue_name = f"test-queue-{short_uid()}"
        queue_url = sqs_create_queue(QueueName=queue_name)
        queue_arn = sqs_get_queue_arn(queue_url)

        # setup topic
        topic_name = f"test-topic-{short_uid()}"
        topic_arn = sns_create_topic(Name=topic_name)["TopicArn"]

        sns_subscription(TopicArn=topic_arn, Protocol="sqs", Endpoint=queue_arn)

        # allow topic to write to sqs queue
        sns_allow_topic_sqs_queue(
            sqs_queue_url=queue_url, sqs_queue_arn=queue_arn, sns_topic_arn=topic_arn
        )

        # publish message
        aws_client.sns.publish(TopicArn=topic_arn, Message=json.dumps(MESSAGE))

        list_events_response = assert_list_events_len(2)
        snapshot_with_default_transformers.add_transformers_list(
            [
                snapshot.transform.regex(queue_name, "test-queue-name"),
                snapshot.transform.regex(topic_arn, "test-topic-arn"),
            ],
        )
        snapshot.match("list_event_response", list_events_response)

        event_to_replay = list_events_response["events"][0]
        assert event_to_replay["operation_name"] == "publish_to_topic"
        assert event_to_replay["is_replayable"] is True

        trace_graph_response = get_trace_graph(event_to_replay["trace_id"])
        snapshot.match("trace_graph_response", trace_graph_response)

        replay_events_response = replay_events({"events": [event_to_replay]})
        assert replay_events_response.status_code == 200

        list_events_response_after_replay = assert_list_events_len(
            5
        )  # +1 since replay operation is also an event that is captured
        snapshot.match("list_event_response_after_replay", list_events_response_after_replay)

        # check update trace graph
        trace_graph_response_after_replay = get_trace_graph(event_to_replay["trace_id"])
        snapshot.match("trace_graph_response_after_replay", trace_graph_response_after_replay)

    def test_replay_s3_single_event(
        self,
        aws_client,
        s3_create_bucket,
        snapshot_with_default_transformers,
        snapshot,
    ):
        # setup bucket
        bucket_name = s3_create_bucket()

        # put object
        test_key = "test-key"
        aws_client.s3.put_object(Bucket=bucket_name, Key=test_key, Body=json.dumps(MESSAGE))

        # check that s3 object is created
        def read_s3_object():
            response = aws_client.s3.list_objects_v2(Bucket=bucket_name)
            assert response["KeyCount"] == 1
            assert response["Contents"][0]["Key"] == test_key
            response = aws_client.s3.get_object(Bucket=bucket_name, Key=test_key)
            assert response["Body"].read().decode("utf-8") == json.dumps(MESSAGE)

        retry(read_s3_object, retries=10, sleep=1)

        list_events_response = assert_list_events_len(1)
        assert list_events_response["events"][0]["operation_name"] == "put_object"
        snapshot_with_default_transformers.add_transformers_list(
            [
                snapshot.transform.regex(bucket_name, "test-bucket-name"),
            ],
        )
        snapshot.match("list_event_response", list_events_response)

        event_to_replay = list_events_response["events"][0]
        assert event_to_replay["operation_name"] == "put_object"
        assert event_to_replay["is_replayable"] is True

        trace_graph_response = get_trace_graph(event_to_replay["trace_id"])
        snapshot.match("trace_graph_response", trace_graph_response)

        # replay_events_response = replay_events({"events": [event_to_replay]})
        # assert replay_events_response.status_code == 200

        # list_events_response_after_replay = assert_list_events_len(3)
        # snapshot.match("list_event_response_after_replay", list_events_response_after_replay)

        # # check update trace graph
        # trace_graph_response_after_replay = get_trace_graph(event_to_replay["trace_id"])
        # snapshot.match("trace_graph_response_after_replay", trace_graph_response_after_replay)
