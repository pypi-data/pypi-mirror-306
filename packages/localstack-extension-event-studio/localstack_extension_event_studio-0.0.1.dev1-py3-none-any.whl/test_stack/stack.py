import os

import aws_cdk as cdk
import aws_cdk.aws_events as events
import aws_cdk.aws_events_targets as events_targets
import aws_cdk.aws_iam as iam
import aws_cdk.aws_lambda as _lambda
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_sns as sns
import aws_cdk.aws_sns_subscriptions as sns_subs
import aws_cdk.aws_sqs as sqs
from constructs import Construct
from dotenv import load_dotenv

load_dotenv()

REGION = os.getenv("REGION")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")
EVENT_BUS_NAME = os.getenv("EVENT_BUS_NAME")
BUCKET_NAME = os.getenv("BUCKET_NAME")


LAMBDA_INLINE_CODE = """
import json
import os

import boto3

s3 = boto3.client("s3")
sqs = boto3.client("sqs")
sns = boto3.client("sns")

BUCKET_NAME = os.getenv("BUCKET_NAME")
QUEUE_URL = os.getenv("QUEUE_URL")
TOPIC_ARN = os.getenv("TOPIC_ARN")


def handler(event, context):
    for record in event["Records"]:
        message_body = record["body"]
        message_id = record["messageId"]

        # Write message body to S3 bucket
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=f"{message_id}.json",
            Body=json.dumps(json.loads(message_body)),
        )

        # Publish a success message to SNS topic
        sns.publish(
            TopicArn=TOPIC_ARN,
            Message=json.dumps(message_body),
            MessageStructure="string",
            Subject="Message Processed Successfully",
        )

        # Delete message from SQS queue
        sqs.delete_message(
            QueueUrl=QUEUE_URL,
            ReceiptHandle=record["receiptHandle"],
        )

    return {"statusCode": 200}
"""


class TestStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Event bus
        event_bus = events.EventBus(self, id="EventBus", event_bus_name=EVENT_BUS_NAME)
        event_bus_two = events.EventBus(self, id="EventBusTwo", event_bus_name="EventBusTwo")
        event_bus_three = events.EventBus(self, id="EventBusThree", event_bus_name="EventBusThree")

        # Sqs queue as target for all events
        sqs_queue = sqs.Queue(self, "Queue", queue_name="MainQueue")
        sqs_queue.add_to_resource_policy(
            iam.PolicyStatement(
                actions=["sqs:SendMessage"],
                effect=iam.Effect.ALLOW,
                resources=[sqs_queue.queue_arn],
                principals=[iam.ServicePrincipal("events.amazonaws.com")],
            )
        )

        # Rule to send all events from event bus primary to sqs queue
        events.Rule(
            self,
            id="RuleEventBus",
            event_bus=event_bus,
            event_pattern=events.EventPattern(source=events.Match.prefix("")),  # matches all events
            targets=[
                events_targets.SqsQueue(sqs_queue),
                events_targets.EventBus(event_bus_two),
                events_targets.EventBus(event_bus_three),
            ],
        )

        # Second event bus
        events.Rule(
            self,
            id="RuleEventBusTwo",
            event_bus=event_bus_two,
            event_pattern=events.EventPattern(source=events.Match.prefix("")),  # matches all events
            targets=[events_targets.SqsQueue(sqs_queue)],
        )

        # Third event bus
        events.Rule(
            self,
            id="RuleEventBusThree",
            event_bus=event_bus_three,
            event_pattern=events.EventPattern(source=events.Match.prefix("")),  # matches all events
            targets=[events_targets.SqsQueue(sqs_queue)],
        )

        # S3 bucket as target for lambda
        bucket = s3.Bucket(self, "Bucket", bucket_name=BUCKET_NAME)

        # SNS topic as target for lambda
        topic = sns.Topic(self, "Topic", topic_name="SuccessTopic")

        # Lambda function to process events
        lambda_function = _lambda.Function(
            self,
            "LambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=_lambda.Code.from_inline(LAMBDA_INLINE_CODE),  # from_asset("lambda"),
            environment={
                "BUCKET_NAME": bucket.bucket_name,
                "QUEUE_URL": sqs_queue.queue_url,
                "TOPIC_ARN": topic.topic_arn,
            },
        )

        # Grant Lambda function permission to read from SQS queue
        sqs_queue.grant_consume_messages(lambda_function)

        # Grant Lambda function permission to write to S3 bucket
        bucket.grant_put(lambda_function)

        # Grant Lambda function permission to publish to SNS topic
        topic.grant_publish(lambda_function)

        # Create event source mapping to trigger Lambda function on SQS queue
        _lambda.EventSourceMapping(
            self,
            "EventSourceMapping",
            event_source_arn=sqs_queue.queue_arn,
            target=lambda_function,
            batch_size=1,
            starting_position=_lambda.StartingPosition.LATEST,
        )

        # Create a new SQS queue to subscribe to the SNS topic
        sns_queue = sqs.Queue(self, "SnsQueue", queue_name="SnsQueue")
        topic.add_subscription(sns_subs.SqsSubscription(sns_queue))

        # Grant necessary permissions for the SNS queue to receive messages
        sns_queue.add_to_resource_policy(
            iam.PolicyStatement(
                actions=["sqs:SendMessage"],
                effect=iam.Effect.ALLOW,
                resources=[sns_queue.queue_arn],
                principals=[iam.ServicePrincipal("sns.amazonaws.com")],
            )
        )

        #########
        # Outputs
        #########
        cdk.CfnOutput(self, "EventBusName", value=event_bus.event_bus_name)
        cdk.CfnOutput(self, "EventBusTwoName", value=event_bus_two.event_bus_name)
        cdk.CfnOutput(self, "EventBusThreeName", value=event_bus_three.event_bus_name)
        cdk.CfnOutput(self, "SQSQueueURL", value=sqs_queue.queue_url)
        cdk.CfnOutput(self, "LambdaFunctionName", value=lambda_function.function_name)
