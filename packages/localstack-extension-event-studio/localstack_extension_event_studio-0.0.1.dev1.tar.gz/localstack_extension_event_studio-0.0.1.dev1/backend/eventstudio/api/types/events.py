from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, model_validator

from eventstudio.api.types.errors import ErrorModel
from eventstudio.api.types.services import ServiceName

RegionName = str


class EventsEventData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: str
    detail_type: str
    source: str
    resources: list[str] | None
    detail: dict[str, str | dict | list]


class EventsEventPartialData(BaseModel):  # required for input validation error of eventbridge
    model_config = ConfigDict(extra="forbid")

    version: str
    detail_type: str | None
    source: str | None
    resources: list[str] | None
    detail: dict[str, str | dict | list] | None


class EventsEventMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_bus_name: str
    replay_name: str | None = None
    original_time: datetime | None = None


class LambdaEventData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payload: dict | str | None = None


class LambdaEventMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    function_name: str
    invocation_type: Literal["RequestResponse", "Event", "DryRun"] = "RequestResponse"
    log_type: str | None = None
    qualifier: str | None = None
    client_context: str | None = None


class SNSEventData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: dict | str


class SNSEventMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message_group_id: str | None = None
    message_structure: Literal["json"] | None = None

    topic_arn: str


class SQSEventData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    body: dict


class SQSEventMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    queue_arn: str

    message_attributes: dict | None = None
    message_system_attributes: dict | None = None
    original_time: datetime | None = None


class S3EventData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    body: str  # TODO update model to store also byte object bytes


class S3EventMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    bucket: str
    key: str


class InputEventModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    parent_id: str | None = None
    trace_id: str | None = None
    event_id: str | None = None

    version: int = 0
    status: str = "OK"
    is_deleted: bool = False
    is_replayable: bool = False
    is_edited: bool = False

    account_id: str
    region: str
    service: ServiceName
    operation_name: str
    creation_time: datetime | None = None

    event_data: (
        EventsEventData
        | EventsEventPartialData
        | LambdaEventData
        | SNSEventData
        | SQSEventData
        | S3EventData
        | None
    ) = None

    event_metadata: (
        EventsEventMetadata
        | LambdaEventMetadata
        | SNSEventMetadata
        | SQSEventMetadata
        | S3EventMetadata
        | None
    ) = None

    @model_validator(mode="after")
    def validate_event_data(cls, values):
        service = values.service
        event_data = values.event_data

        if service == ServiceName.EVENTS and not isinstance(
            event_data, (EventsEventData, EventsEventPartialData)
        ):
            raise ValueError(
                'For service "events", event_data must be of type EventsData or EventsEventPartialData.'
            )
        elif service == ServiceName.LAMBDA and not isinstance(event_data, LambdaEventData):
            raise ValueError('For service "lambda", event_data must be of type LambdaEventData.')
        elif service == ServiceName.SNS and not isinstance(event_data, SNSEventData):
            raise ValueError('For service "sns", event_data must be of type SNSEventData.')
        elif service == ServiceName.SQS and not isinstance(event_data, SQSEventData):
            raise ValueError('For service "sqs", event_data must be of type SQSEventData.')
        elif service == ServiceName.S3 and not isinstance(event_data, S3EventData):
            raise ValueError('For service "s3", event_data must be of type S3EventData.')

        return values

    @model_validator(mode="after")
    def validate_event_metadata(cls, values):
        service = values.service
        event_metadata = values.event_metadata

        if service == ServiceName.EVENTS and not isinstance(event_metadata, EventsEventMetadata):
            raise ValueError('For service "events", event_metadata must be of type EventsMetadata.')
        elif service == ServiceName.LAMBDA and not isinstance(event_metadata, LambdaEventMetadata):
            raise ValueError(
                'For service "lambda", event_metadata must be of type LambdaEventMetadata.'
            )
        elif service == ServiceName.SQS and not isinstance(event_metadata, SQSEventMetadata):
            raise ValueError('For service "sqs", event_metadata must be of type SQSEventMetadata.')
        elif service == ServiceName.SNS and not isinstance(event_metadata, SNSEventMetadata):
            raise ValueError('For service "sns", event_metadata must be of type SNSEventMetadata.')
        elif service == ServiceName.S3 and not isinstance(event_metadata, S3EventMetadata):
            raise ValueError('For service "s3", event_metadata must be of type S3EventMetadata.')

        return values


class InputEventModelList(BaseModel):
    events: list[InputEventModel]


class EventModel(InputEventModel):
    model_config = ConfigDict(from_attributes=True)

    span_id: str
    errors: list["ErrorModel"] = []

    children: list["EventModel"] = []


class EventModelList(BaseModel):
    events: list[EventModel]
