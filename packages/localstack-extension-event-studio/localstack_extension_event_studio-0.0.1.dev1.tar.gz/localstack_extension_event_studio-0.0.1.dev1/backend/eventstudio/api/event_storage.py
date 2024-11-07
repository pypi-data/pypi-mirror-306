import logging

import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from eventstudio.api.event_streamer import EventStreamer
from eventstudio.api.models import ErrorDBModel, EventDBModel, TraceLinkDBModel, get_engine
from eventstudio.api.types.errors import InputErrorModel
from eventstudio.api.types.events import (
    EventModel,
    EventModelList,
    InputEventModel,
)
from eventstudio.api.types.responses import Error, FailedEntry
from eventstudio.api.types.trace_context import TraceContext

LOG = logging.getLogger(__name__)


class EventStorageService:
    def __init__(self, db_path: str = "", event_streamer: EventStreamer | None = None):
        self._engine = get_engine(db_path)
        self._event_streaming_service: EventStreamer | None = event_streamer

    def add_event(self, event: InputEventModel) -> tuple[str, str] | Error:
        try:
            with Session(self._engine) as session:
                event_model = EventDBModel(**event.model_dump())
                session.add(event_model)
                session.commit()
                if self._event_streaming_service:
                    event = EventModel.model_validate(event_model, from_attributes=True)
                    self._event_streaming_service.notify(event)
                return event_model.span_id, event_model.trace_id
        except Exception as e:
            LOG.error(f"Failed to add event: {e}")
            return {"error": e}

    def add_error(self, error: InputErrorModel):
        with Session(self._engine) as session:
            error_model = ErrorDBModel(**error.model_dump())
            session.add(error_model)
            session.commit()

            if self._event_streaming_service:
                span_id = error_model.span_id
                # Retrieve event associated with the error
                event = self.get_event(span_id)
                self._event_streaming_service.notify(event)

    def list_events(self) -> list[EventModel]:
        with Session(self._engine) as session:
            events = session.query(EventDBModel).all()
            events = [EventModel.model_validate(event) for event in events]

        event_dict = {event.span_id: event for event in events}

        for event in events:
            self._set_children(event, event_dict)

        for event in events:
            self._get_latest_event(event)

        return events

    def get_event(self, span_id: str) -> EventModel | None:
        try:
            with Session(self._engine) as session:
                event = session.query(EventDBModel).filter(EventDBModel.span_id == span_id).first()

                if not event:
                    return None

                return EventModel.model_validate(event)

        except Exception as e:
            LOG.error(f"Failed to get event: {e}")
            return {"error": e, "span_id": span_id}

    def delete_event(self, span_id: str) -> FailedEntry | None:
        try:
            with Session(self._engine) as session:
                stm = sa.delete(EventDBModel).where(EventDBModel.span_id == span_id)
                session.execute(stm)
                session.commit()
        except Exception as e:
            LOG.error(f"Failed to delete event: {e}")
            return {"error": e, "span_id": span_id}

    def delete_all_events(self) -> Error | None:
        try:
            with Session(self._engine) as session:
                session.query(EventDBModel).delete()
                session.commit()
        except Exception as e:
            LOG.error(f"Failed to delete all events: {e}")
            return {"error": e}

    def list_events_graph(self) -> EventModelList:
        with Session(self._engine) as session:
            events = session.query(EventDBModel).all()
            events = [EventModel.model_validate(event) for event in events]

        event_dict = {event.span_id: event for event in events}

        for event in events:
            if event.parent_id and event.parent_id in event_dict:
                parent = event_dict[event.parent_id]
                parent.children.append(event)

        return EventModelList(events=events)

    def get_event_graph(self, trace_id: str | None) -> EventModel | None:
        with Session(self._engine) as session:
            events = session.query(EventDBModel).where(EventDBModel.trace_id == trace_id).all()
            events = [EventModel.model_validate(event) for event in events]

        root_event = None
        event_graph = {}
        for event in events:
            if event.parent_id is None:
                root_event = event
            event_graph[event.span_id] = event

        for event in events:
            if event.parent_id is None:
                continue
            event_graph[event.parent_id].children.append(event)

        updated_root_event = self._get_latest_event(root_event)

        return updated_root_event

    def store_xray_trace(self, xray_trace_id: str, trace_context: TraceContext) -> None | Error:
        try:
            with Session(self._engine) as session:
                trace_link = TraceLinkDBModel(
                    xray_trace_id=xray_trace_id,
                    parent_id=trace_context.parent_id,
                    trace_id=trace_context.trace_id,
                )
                session.add(trace_link)
                session.commit()
                return None

        except SQLAlchemyError as e:
            error_msg = f"Database error while storing XRay trace {xray_trace_id}: {str(e)}"
            LOG.error(error_msg)
            return Error(error=error_msg)

        except Exception as e:
            error_msg = f"Unexpected error while storing XRay trace {xray_trace_id}: {str(e)}"
            LOG.error(error_msg)
            return Error(error=error_msg)

    def get_trace_from_xray_trace(self, xray_trace_id: str) -> tuple[str, str] | None | Error:
        """Retrieve the trace_id and parent_id associated with an XRay trace ID."""
        try:
            with Session(self._engine) as session:
                trace_link = (
                    session.query(TraceLinkDBModel)
                    .filter(TraceLinkDBModel.xray_trace_id == xray_trace_id)
                    .first()
                )

                if not trace_link:
                    LOG.debug(f"No trace link found for XRay trace ID: {xray_trace_id}")
                    return None

                return (trace_link.trace_id, trace_link.parent_id)

        except SQLAlchemyError as e:
            error_msg = (
                f"Database error while retrieving event for XRay trace {xray_trace_id}: {str(e)}"
            )
            LOG.error(error_msg)
            return Error(error=error_msg)

        except Exception as e:
            error_msg = (
                f"Unexpected error while retrieving event for XRay trace {xray_trace_id}: {str(e)}"
            )
            LOG.error(error_msg)
            return Error(error=error_msg)

    def get_event_by_id(self, event_id: str) -> EventModel | Error | None:
        try:
            with Session(self._engine) as session:
                event = (
                    session.query(EventDBModel).filter(EventDBModel.event_id == event_id).first()
                )

                if not event:
                    return None

                return EventModel.model_validate(event)

        except Exception as e:
            error_message = f"Failed to get event with message_id {event_id}: {e}"
            LOG.error(error_message)
            return Error(error=error_message)

    def _set_children(self, event: EventModel, event_dict: dict[str, EventModel]) -> None:
        if event.parent_id and event.parent_id in event_dict:
            parent = event_dict[event.parent_id]
            parent.children.append(event)

    def _get_latest_event(self, event: EventModel) -> EventModel:
        """Replayed events are stored as new events linked via parent_id to the event that is initially replayed.
        Furthermore a replayed event is additionally captured a second time in the extension when it flows through localstack.
        A replayed event would look like this in the database: original_event_operation -> replayed_event -> replayed_event_operation.
        The graph should only show the replayed_event_operation with an incremented version number.
        This method traverses the graph to find the latest version of the event and remove the duplicate.
        """
        if not event.children:
            return event

        latest_event = max(event.children, key=lambda e: e.version)
        if latest_event.version > event.version and latest_event.operation_name == "replay_event":
            if not latest_event.children:
                return latest_event
            event = latest_event.children[0].model_copy(deep=True)
            event.version = latest_event.version

        # Recursively update all children
        event.children = [self._get_latest_event(child) for child in event.children]
        return event
