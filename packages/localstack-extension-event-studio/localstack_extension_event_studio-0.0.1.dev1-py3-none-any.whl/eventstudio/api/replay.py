import json
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from botocore.client import BaseClient
from localstack.aws.api.events import AccountId, PutEventsRequestEntry, PutEventsResponse
from localstack.aws.connect import connect_to

from eventstudio.api.event_storage import EventStorageService
from eventstudio.api.types.errors import ErrorType, InputErrorModel
from eventstudio.api.types.events import (
    EventModel,
    RegionName,
)
from eventstudio.api.types.services import ServiceName
from eventstudio.api.types.trace_context import TraceContext
from eventstudio.api.utils.arn_utils import get_queue_url_from_arn
from eventstudio.constants import INTERNAL_REQUEST_TRACE_HEADER


class ReplayEventSender(ABC):
    service: ServiceName
    account_id: AccountId
    region: RegionName

    def __init__(
        self,
        service: ServiceName,
        account_id: AccountId,
        region: RegionName,
        event_studio_service: EventStorageService,
    ):
        self.service = service
        self.account_id = account_id
        self.region = region
        self._client: BaseClient | None = None
        self._event_studio_service: EventStorageService = event_studio_service

    @property
    def client(self):
        """Lazy initialization of internal botoclient factory."""
        if self._client is None:
            self._client = self._initialize_client()
        return self._client

    def _initialize_client(self) -> BaseClient:
        """Initializes internal boto client."""
        client_factory = connect_to(aws_access_key_id=self.account_id, region_name=self.region)
        client = client_factory.get_client(self.service.value)
        return client

    def _set_headers(self, event: EventModel):
        def _handler_inject_replay_trace_header(
            params: dict[str, Any], context: dict[str, Any], **kwargs
        ):
            trace_context = TraceContext(
                trace_id=event.trace_id, parent_id=event.span_id, version=event.version
            )
            params["headers"][INTERNAL_REQUEST_TRACE_HEADER] = trace_context.model_dump_json()

        self.client.meta.events.register(
            "before-call.*.*", handler=_handler_inject_replay_trace_header
        )

        def _error_highlighting(exception, **kwargs):
            if exception is not None:
                error = InputErrorModel(
                    error_type=ErrorType.BOTO_ERROR,
                    error_text=str(exception),
                    span_id=event.span_id,
                )
                self._event_studio_service.add_error(error)

        self.client.meta.events.register("after-call-error", handler=_error_highlighting)

    def replay_event(self, event: EventModel) -> dict[str, str]:
        self._set_headers(event)
        return self.send_event(event)

    @abstractmethod
    def send_event(self, event: EventModel) -> dict[str, str]:
        """Sends event to the service."""
        pass


class EventsReplayEventSender(ReplayEventSender):
    def _re_format_event(self, event: EventModel) -> PutEventsRequestEntry:
        event_data = event.event_data
        event_metadata = event.event_metadata
        re_formatted_event = {
            "Source": event_data.source,
            "DetailType": event_data.detail_type,
            "Detail": json.dumps(event_data.detail),
            "Time": event.creation_time.isoformat()
            if event.creation_time
            else datetime.now().isoformat(),
            "EventBusName": event_metadata.event_bus_name,
        }
        if event_data.resources:
            re_formatted_event["Resources"] = str(event_data.resources)
        if event_metadata.replay_name:
            re_formatted_event["ReplayName"] = event_data.replay_name

        return PutEventsRequestEntry(**re_formatted_event)

    def send_event(self, event: EventModel) -> PutEventsResponse:
        re_formatted_event = self._re_format_event(event)
        response = self.client.put_events(Entries=[re_formatted_event])
        return response


class LambdaReplayEventSender(ReplayEventSender):
    def send_event(self, event: EventModel) -> dict[str, str]:
        function_name = event.event_metadata.function_name
        payload = event.event_data.payload
        invocation_type = event.event_metadata.invocation_type
        response = self.client.invoke(
            FunctionName=function_name,
            InvocationType=invocation_type,
            Payload=json.dumps(payload),
        )
        return response


class SnsReplayEventSender(ReplayEventSender):
    def send_event(self, event: EventModel) -> dict[str, str]:
        topic_arn = event.event_metadata.topic_arn
        message = event.event_data.message.get("message")
        response = self.client.publish(TopicArn=topic_arn, Message=json.dumps(message))
        return response


class SqsReplayEventSender(ReplayEventSender):
    def send_event(self, event: EventModel) -> dict[str, str]:
        queue_url = get_queue_url_from_arn(event.event_metadata.queue_arn)
        message_body = event.event_data.body
        response = self.client.send_message(
            QueueUrl=queue_url, MessageBody=json.dumps(message_body)
        )
        return response


class ReplayEventSenderFactory:
    service: ServiceName
    account_id: AccountId
    region: RegionName

    service_map = {
        ServiceName.EVENTS: EventsReplayEventSender,
        ServiceName.LAMBDA: LambdaReplayEventSender,
        ServiceName.SNS: SnsReplayEventSender,
        ServiceName.SQS: SqsReplayEventSender,
    }

    def __init__(
        self,
        service: ServiceName,
        account_id: AccountId,
        region: RegionName,
        event_studio_service: EventStorageService,
    ):
        self.service = service
        self.account_id = account_id
        self.region = region
        self.event_studio_service: EventStorageService = event_studio_service

    def get_sender(self) -> ReplayEventSender:
        return self.service_map[self.service](
            service=self.service,
            account_id=self.account_id,
            region=self.region,
            event_studio_service=self.event_studio_service,
        )
