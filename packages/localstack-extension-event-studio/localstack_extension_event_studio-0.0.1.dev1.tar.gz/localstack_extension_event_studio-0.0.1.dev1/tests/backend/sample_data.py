import json
import uuid

from localstack.utils.strings import long_uid

EVENT_NO_EVENT_BUS_NAME = {
    "Source": "core.update-account-command",
    "DetailType": "core.update-account-command",
    "Detail": json.dumps({"command": ["update-account"]}),
}

NEW_RAW_EVENT_EVENTS_DATA = {
    "version": "0",
    "detail_type": "sampleDetailType",
    "source": "make-put-event",
    "resources": [],
    "detail": {"key": "value"},
}
NEW_RAW_EVENT_EVENTS_METADATA = {"event_bus_name": "default"}

NEW_RAW_EVENT_LAMBDA_DATA = {
    "payload": {"key": "value"},
}
NEW_RAW_EVENT_LAMBDA_METADATA = {
    "function_name": "test-function",
    "invocation_type": "RequestResponse",
    "log_type": "test",
    "qualifier": "test",
    "client_context": "test",
}

NEW_RAW_EVENT_SNS_DATA = {
    "message": {"key": "value"},
}
NEW_RAW_EVENT_SNS_METADATA = {
    "message_group_id": "test",
    "message_structure": "json",
    "topic_arn": "arn:aws:sns:us-east-1:000000000000:MyTopic",
}

NEW_RAW_EVENT_SQS_DATA = {
    "body": {"key": "value"},
}
NEW_RAW_EVENT_SQS_METADATA = {
    "queue_arn": "arn:aws:sqs:us-east-1:000000000000:MyQueue",
    "message_attributes": {"key": "value"},
    "message_system_attributes": {"key": "value"},
}

NEW_RAW_EVENT_S3_DATA = {
    "body": "test",
}

NEW_RAW_EVENT_S3_METADATA = {
    "bucket": "testbucket",
    "key": "testkey",
}

NEW_RAW_EVENT = {
    "event_id": str(long_uid()),
    "version": 0,
    "status": "OK",
    "is_deleted": False,
    "is_replayable": False,
    "is_edited": False,
    "account_id": "000000000000",
    "region": "us-east-1",
    "creation_time": "2024-08-02T13:28:51.476Z",
}

new_raw_event_events = {
    **NEW_RAW_EVENT,
    "service": "events",
    "operation_name": "raw_input_event",
    "event_data": NEW_RAW_EVENT_EVENTS_DATA,
    "event_metadata": NEW_RAW_EVENT_EVENTS_METADATA,
}

new_raw_event_lambda = {
    **NEW_RAW_EVENT,
    "service": "lambda",
    "operation_name": "lambda_invoke",
    "event_data": NEW_RAW_EVENT_LAMBDA_DATA,
    "event_metadata": NEW_RAW_EVENT_LAMBDA_METADATA,
}

new_raw_event_sns = {
    **NEW_RAW_EVENT,
    "service": "sns",
    "operation_name": "sns_publish",
    "event_data": NEW_RAW_EVENT_SNS_DATA,
    "event_metadata": NEW_RAW_EVENT_SNS_METADATA,
}

new_raw_event_sqs = {
    **NEW_RAW_EVENT,
    "service": "sqs",
    "operation_name": "sqs_send_message",
    "event_data": NEW_RAW_EVENT_SQS_DATA,
    "event_metadata": NEW_RAW_EVENT_SQS_METADATA,
}

new_raw_event_s3 = {
    **NEW_RAW_EVENT,
    "service": "s3",
    "operation_name": "s3_put_object",
    "event_data": NEW_RAW_EVENT_S3_DATA,
    "event_metadata": NEW_RAW_EVENT_S3_METADATA,
}


MESSAGE = {
    "key": {"DataType": "String", "StringValue": "value"},
}


new_database_event_events = {
    **new_raw_event_events,
    "span_id": str(uuid.uuid4()),
    "trace_id": str(uuid.uuid4()),
    "parent_id": str(uuid.uuid4()),
}

new_database_event_lambda = {
    **new_raw_event_lambda,
    "span_id": str(uuid.uuid4()),
    "trace_id": str(uuid.uuid4()),
    "parent_id": str(uuid.uuid4()),
}

new_database_event_sns = {
    **new_raw_event_sns,
    "span_id": str(uuid.uuid4()),
    "trace_id": str(uuid.uuid4()),
    "parent_id": str(uuid.uuid4()),
}

new_database_event_sqs = {
    **new_raw_event_sqs,
    "span_id": str(uuid.uuid4()),
    "trace_id": str(uuid.uuid4()),
    "parent_id": str(uuid.uuid4()),
}

new_database_event_s3 = {
    **new_raw_event_s3,
    "span_id": str(uuid.uuid4()),
    "trace_id": str(uuid.uuid4()),
    "parent_id": str(uuid.uuid4()),
}
