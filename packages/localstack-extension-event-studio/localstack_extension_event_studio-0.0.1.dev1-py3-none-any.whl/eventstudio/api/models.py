import os.path
import sqlite3
import time
import uuid
from datetime import datetime, timezone
from functools import partial

import sqlalchemy as sa
from localstack.utils.strings import short_uid
from sqlalchemy import Enum
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import declarative_base, relationship

from eventstudio.api.types.errors import ErrorType
from eventstudio.api.types.services import ServiceName
from eventstudio.api.utils.utils import CustomJSONEncoder, JSONEncodedDict

Base = declarative_base()


class EventDBModel(Base):
    __tablename__ = "events"
    span_id = sa.Column(sa.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    parent_id = sa.Column(sa.String, sa.ForeignKey("events.span_id"), nullable=True)
    trace_id = sa.Column(sa.String, nullable=False, default=lambda: str(uuid.uuid4()))

    event_id = sa.Column(sa.String)

    # we might want later to easily load children nodes, not needed for now
    # children = relationship("EventDBModel")

    is_deleted = sa.Column(sa.Boolean, default=False, nullable=False)
    creation_time = sa.Column(
        sa.DateTime, nullable=False, default=partial(datetime.now, tz=timezone.utc)
    )
    status = sa.Column(sa.String, default="OK", nullable=False)

    account_id = sa.Column(sa.String, nullable=False)
    region = sa.Column(sa.String, nullable=False)
    service = sa.Column(Enum(ServiceName), nullable=False)
    operation_name = sa.Column(sa.String, nullable=False)

    errors = relationship("ErrorDBModel", back_populates="events")

    version = sa.Column(sa.Integer, nullable=False, default=0)
    is_replayable = sa.Column(sa.Boolean, nullable=False, default=False)
    is_edited = sa.Column(sa.Boolean, nullable=False, default=False)

    event_data = sa.Column(JSONEncodedDict(encoder=CustomJSONEncoder), nullable=False)
    event_metadata = sa.Column(JSONEncodedDict(encoder=CustomJSONEncoder))


class TraceLinkDBModel(Base):
    __tablename__ = "trace_links"

    xray_trace_id = sa.Column(sa.String, primary_key=True, nullable=False, unique=True)
    parent_id = sa.Column(sa.String, sa.ForeignKey("events.span_id"), nullable=False)
    trace_id = sa.Column(sa.String, sa.ForeignKey("events.trace_id"), nullable=False)


class ErrorDBModel(Base):
    __tablename__ = "errors"
    error_id = sa.Column(sa.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    span_id = sa.Column(sa.String, sa.ForeignKey("events.span_id"), nullable=False)

    error_message = sa.Column(sa.String, nullable=False)
    error_type = sa.Column(Enum(ErrorType), nullable=False)
    creation_time = sa.Column(
        sa.DateTime, nullable=False, default=partial(datetime.now, tz=timezone.utc)
    )

    events = relationship("EventDBModel", back_populates="errors")


def get_engine(db_path: str) -> Engine:
    # try to get writable db file or use new db_path after timeout
    db_path = check_and_close_sqlite_db(db_path)

    engine = create_engine(f"sqlite:///{db_path}", echo=True)
    Base.metadata.create_all(engine)
    return engine


def check_and_close_sqlite_db(db_path: str, max_attempts=10, wait_time=5):
    if not os.path.isfile(db_path):
        return db_path

    for attempt in range(max_attempts):
        try:
            # Attempt to open the database with immediate mode
            with sqlite3.connect(db_path, timeout=1, isolation_level="IMMEDIATE"):
                # If we get here, the database isn't locked
                print(f"Successfully opened {db_path}")
                return db_path

        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                print(f"Attempt {attempt + 1}: Database is locked. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"An operational error occurred: {e}")

    # we weren't able to obtain lock
    return db_path + short_uid()
