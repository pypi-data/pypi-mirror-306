import json
import os

import boto3


def handler(event, context):
    # put event to sqs queue
    sqs = boto3.client("sqs")
    queue_url = os.environ["QUEUE_URL"]
    sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(event))
