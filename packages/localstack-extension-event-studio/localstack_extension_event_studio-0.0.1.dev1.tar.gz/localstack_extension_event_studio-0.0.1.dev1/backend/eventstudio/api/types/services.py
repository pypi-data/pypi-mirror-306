from enum import Enum


class ServiceName(Enum):
    EVENTS = "events"
    EVENT_STUDIO = "event_studio"
    SQS = "sqs"
    LAMBDA = "lambda"
    SNS = "sns"
    S3 = "s3"
