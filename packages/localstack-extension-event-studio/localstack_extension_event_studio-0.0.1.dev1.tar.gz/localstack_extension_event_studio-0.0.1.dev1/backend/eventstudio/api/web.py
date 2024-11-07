import logging

import botocore.exceptions
from botocore.client import BaseClient
from localstack.aws.api.events import AccountId
from localstack.http import Request, Response, route

from eventstudio.api.config import Config
from eventstudio.api.event_storage import EventStorageService
from eventstudio.api.replay import ReplayEventSender, ReplayEventSenderFactory
from eventstudio.api.types.errors import ErrorType, InputErrorModel
from eventstudio.api.types.events import (
    EventModel,
    EventModelList,
    InputEventModel,
    InputEventModelList,
    RegionName,
)
from eventstudio.api.types.requests import DeleteEventsRequest
from eventstudio.api.types.responses import (
    AddEventsResponse,
    DeleteAllEventsResponse,
    DeleteEventsResponse,
    GetEventResponse,
    ListEventsResponse,
    ReplayEventsResponse,
    TraceGraphResponse,
)
from eventstudio.api.types.services import ServiceName
from eventstudio.api.utils.utils import parse_request_body

from .. import static
from .event_streamer import EventStreamer

LOG = logging.getLogger(__name__)


class WebApp:
    def __init__(self, event_storage_service: EventStorageService, event_streamer: EventStreamer):
        self._event_storage_service: EventStorageService = event_storage_service
        self._clients: dict[tuple[AccountId, RegionName], BaseClient] = {}
        self._replay_event_sender_store = {}
        self._event_streamer = event_streamer

    ###############################
    # Frontend served via extension
    ###############################
    @route("/")
    def index(self, request: Request, *args, **kwargs):
        return Response.for_resource(static, "index.html")

    @route("/<path:path>")
    def index2(self, request: Request, path: str, **kwargs):
        return Response.for_resource(static, path)

    ###############
    # API Endpoints
    ###############
    @route(Config.get_relative_url(Config.EVENTS), methods=["WEBSOCKET"])
    def live_stream(self, request, *args, **kwargs):
        return self._event_streamer.on_websocket_request(request, *args, **kwargs)

    @route(Config.get_relative_url(Config.EVENTS), methods=["POST"])
    def add_events(self, request: Request, events: InputEventModelList) -> AddEventsResponse:
        failed_entry_count = 0
        failed_entries = []

        for event in events.events:
            response = self._event_storage_service.add_event(event)

            if isinstance(response, dict) and "error" in response:
                failed_entry_count += 1
                failed_entries.append(response.error)

        if failed_entry_count > 0:
            return AddEventsResponse(
                status=400, FailedEntryCount=failed_entry_count, FailedEntries=failed_entries
            )

        return AddEventsResponse(status=200, FailedEntryCount=0, FailedEntries=[])

    @route(Config.get_relative_url(Config.EVENTS), methods=["DELETE"])
    def delete_events(self, request: Request) -> DeleteEventsResponse:
        body = parse_request_body(request, DeleteEventsRequest)

        failed_entry_count = 0
        failed_entries = []

        for span_id in body.span_ids:
            response = self._event_storage_service.delete_event(span_id=span_id)

            if response:
                failed_entry_count += 1
                failed_entries.append(response)

        if failed_entry_count > 0:
            return DeleteEventsResponse(
                status=400, FailedEntryCount=failed_entry_count, FailedEntries=failed_entries
            )

        return DeleteEventsResponse(status=200, FailedEntryCount=0, FailedEntries=[])

    @route(Config.get_relative_url(Config.ALL_EVENTS), methods=["DELETE"])
    def delete_all_events(self, request: Request) -> DeleteAllEventsResponse:
        response = self._event_storage_service.delete_all_events()
        if response:
            return DeleteAllEventsResponse(status=400, error=response.get("error"))
        return DeleteAllEventsResponse(status=200)

    @route(Config.get_relative_url(Config.EVENTS), methods=["GET"])
    def list_events(self, request: Request) -> ListEventsResponse:
        try:
            events = self._event_storage_service.list_events()
        except Exception as e:
            LOG.error(f"Failed to list events: {e}")
            return ListEventsResponse(
                status=400, error=f"Error occurred while fetching all events: {e}"
            )

        return ListEventsResponse(status=200, events=events)

    @route(f"{Config.get_relative_url(Config.EVENTS)}/<span_id>", methods=["GET"])
    def get_event_details(self, request: Request, span_id: str):
        try:
            event = self._event_storage_service.get_event(span_id)
            if not event:
                return GetEventResponse(
                    status=404, error=f"Event with span_id {span_id} not found."
                )

            return GetEventResponse(status=200, event=event.dict())
        except Exception as e:
            LOG.error("Failed to get event with span_id %s: %s", span_id, e)
            return GetEventResponse(
                status=400, error=f"Error occurred while fetching the event: {e}"
            )

    @route(f"{Config.get_relative_url(Config.TRACES)}/<trace_id>", methods=["GET"])
    def get_trace_graph(self, request: Request, trace_id: str) -> TraceGraphResponse:
        event = self._event_storage_service.get_event_graph(trace_id=trace_id)
        if event is None:
            return TraceGraphResponse(status=404)

        return TraceGraphResponse(status=200, event=event)

    @route(Config.get_relative_url(Config.REPLAY), methods=["POST"])
    def replay_events(self, request: Request, event_list: EventModelList) -> ReplayEventsResponse:
        failed_entry_count = 0
        failed_entries = []

        for event in event_list.events:
            if not event.is_replayable:
                failed_entry_count += 1
                failed_entries.append(event)
                continue

            # enrich event with event data from storage
            event_in_storage = self._event_storage_service.get_event(span_id=event.span_id)
            combined_raw_event = {**event_in_storage.model_dump(), **event.model_dump()}
            combined_input_event = InputEventModel(**combined_raw_event)

            if combined_input_event.version == 0:
                combined_input_event.parent_id = event.span_id

            combined_input_event.operation_name = "replay_event"
            combined_input_event.version += 1
            combined_input_event.is_replayable = False

            span_id, _ = self._event_storage_service.add_event(
                InputEventModel.model_validate(combined_input_event)
            )

            combined_event = EventModel(**combined_input_event.model_dump(), span_id=span_id)

            sender = self.get_replay_event_sender(
                service=combined_event.service,
                account_id=combined_event.account_id,
                region=combined_event.region,
            )
            try:
                response = sender.replay_event(event=combined_event)
            # only client side validation errors are stored here
            except (botocore.exceptions.ParamValidationError, botocore.exceptions.ClientError) as e:
                event_error = InputErrorModel(
                    span_id=combined_event.span_id,
                    error_message=str(e),
                    error_type=ErrorType.BOTO_ERROR,
                )
                self._event_storage_service.add_error(InputErrorModel.model_validate(event_error))
                response = None

            if (
                response and response.get("ResponseMetadata", {}).get("HTTPStatusCode") != 200
            ) or response is None:
                failed_entry_count += 1
                failed_entries.append(combined_event)

        if failed_entry_count > 0:
            return ReplayEventsResponse(
                status=400, FailedEntryCount=failed_entry_count, FailedEntries=failed_entries
            )

        return ReplayEventsResponse(status=200, FailedEntryCount=0, FailedEntries=[])

    #########
    # Helpers
    #########

    def get_replay_event_sender(
        self, service: ServiceName, account_id: AccountId, region: RegionName
    ) -> ReplayEventSender:
        """Returns replay event sender for given service, account_id and region.
        The replay event sender handles transforming the event to the expected format
        and sending it to the respective service."""
        replay_event_sender = ReplayEventSenderFactory(
            service, account_id, region, self._event_storage_service
        ).get_sender()
        self._replay_event_sender_store[(service, account_id, region)] = replay_event_sender
        return replay_event_sender
