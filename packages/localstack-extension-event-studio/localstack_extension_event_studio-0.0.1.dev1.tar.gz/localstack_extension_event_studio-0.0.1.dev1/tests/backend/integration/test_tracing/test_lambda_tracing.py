import json
import os
import time

from localstack.aws.api.lambda_ import Runtime
from localstack.utils.strings import short_uid

from tests.backend.integration.helper_functions import assert_list_events_len
from tests.backend.sample_data import MESSAGE


def test_lambda_tracing_outgoing_calls(
    sqs_create_queue,
    sqs_get_queue_arn,
    create_lambda_function,
    aws_client,
    snapshot_with_default_transformers,
    snapshot,
):
    # lambda to sqs

    # create queue
    queue_name = f"test-queue-{short_uid()}"
    queue_url = sqs_create_queue(QueueName=queue_name)
    queue_arn = sqs_get_queue_arn(queue_url)

    # create lambda
    function_name = f"test-function-{short_uid()}"
    create_lambda_function(
        handler_file=os.path.join(os.path.dirname(os.path.realpath(__file__)), "lambda_handler.py"),
        func_name=function_name,
        runtime=Runtime.python3_12,
        Environment={"Variables": {"QUEUE_URL": queue_url}},
    )

    lambda_config = aws_client.lambda_.get_function_configuration(FunctionName=function_name)
    role_arn = lambda_config["Role"]
    role_name = role_arn.split("/")[-1]

    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:GetQueueAttributes"],
                "Resource": queue_arn,
            }
        ],
    }

    policy_name = f"SQSConsumeMessagesFor{function_name}"
    response = aws_client.iam.create_policy(
        PolicyName=policy_name, PolicyDocument=json.dumps(policy_document)
    )
    policy_arn = response["Policy"]["Arn"]

    aws_client.iam.attach_role_policy(RoleName=role_name, PolicyArn=policy_arn)

    # invoke lambda
    response = aws_client.lambda_.invoke(FunctionName=function_name, Payload=json.dumps(MESSAGE))
    assert response["StatusCode"] == 200

    list_events_response = assert_list_events_len(2)
    assert list_events_response["events"][0]["service"] == "lambda"
    assert len(list_events_response["events"][0]["children"]) == 1

    snapshot_with_default_transformers.add_transformers_list(
        [
            snapshot.transform.regex(queue_name, "test-queue-name"),
            snapshot.transform.regex(function_name, "test-function"),
        ],
    )
    snapshot.match("list_event_response", list_events_response)


def test_lambda_tracing_esm(
    sqs_create_queue,
    sqs_get_queue_arn,
    create_lambda_function,
    create_event_source_mapping,
    aws_client,
    snapshot_with_default_transformers,
    snapshot,
):
    # sqs to lambda via esm

    # create queue
    queue_name = f"test-queue-{short_uid()}"
    queue_url = sqs_create_queue(QueueName=queue_name)
    queue_arn = sqs_get_queue_arn(queue_url)

    # create lambda
    function_name = f"test-function-{short_uid()}"
    create_lambda_function(
        handler_file=os.path.join(os.path.dirname(os.path.realpath(__file__)), "lambda_handler.py"),
        func_name=function_name,
        runtime=Runtime.python3_12,
        Environment={"Variables": {"QUEUE_URL": queue_url}},
    )

    # set up esm
    map_uuid = create_event_source_mapping(
        EventSourceArn=queue_arn,
        FunctionName=function_name,
        MaximumBatchingWindowInSeconds=1,
    )["UUID"]

    # send message to queue
    aws_client.sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(MESSAGE))

    # check events recorded in backend
    list_events_response = assert_list_events_len(3)
    assert list_events_response["events"][0]["service"] == "sqs"
    assert len(list_events_response["events"][0]["children"]) == 1
    assert len(list_events_response["events"][0]["children"][0]["children"]) == 1

    snapshot_with_default_transformers.add_transformers_list(
        [
            snapshot.transform.regex(queue_name, "test-queue-name"),
            snapshot.transform.regex(function_name, "test-function"),
        ]
    )
    snapshot.match("list_event_response", list_events_response)

    # workaround for lambda being deleted before event source mapping
    aws_client.lambda_.delete_event_source_mapping(UUID=map_uuid)
    time.sleep(5)
