import json

from localstack.utils.strings import short_uid

from tests.backend.integration.helper_functions import assert_list_events_len
from tests.backend.sample_data import MESSAGE


def test_sns_outbound_tracing(
    aws_client,
    sqs_create_queue,
    sqs_get_queue_arn,
    sns_create_topic,
    sns_subscription,
    sns_allow_topic_sqs_queue,
    snapshot_with_default_transformers,
    snapshot,
):
    # sns - sqs

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
    assert len(list_events_response["events"][0]["children"]) == 1
    snapshot_with_default_transformers.add_transformers_list(
        [
            snapshot.transform.regex(queue_name, "test-queue-name"),
            snapshot.transform.regex(topic_arn, "test-topic-arn"),
        ],
    )
    snapshot.match("list_event_response", list_events_response)
