import logging

from localstack.utils.xray.trace_header import TraceHeader

from eventstudio.api.event_storage import EventStorageService
from eventstudio.api.types.trace_context import TraceContext
from eventstudio.api.utils.utils import compile_regex_patterns

LOG = logging.getLogger(__name__)


XRAY_TRACE_HEADER_PATTERNS = compile_regex_patterns([r"Root=([^;]+)"])


def extract_xray_trace_id_from_header_str(xray_header: str) -> str | None:
    try:
        if match := XRAY_TRACE_HEADER_PATTERNS[0].search(xray_header):
            x_ray_trace_id = match.group(1)
            return x_ray_trace_id
        else:
            LOG.debug("No X-Ray trace ID found in X-Ray trace header")
            return None
    except KeyError as e:
        LOG.warning(f"Missing required field in X-Ray trace header: {e}")
        return None
    except Exception as e:
        LOG.warning(f"Error extracting X-Ray trace ID: {e}")
        return None


def extract_aws_trace_header(trace_context: dict) -> TraceHeader | None:
    try:
        aws_trace_header = trace_context.get("aws_trace_header")
        if not aws_trace_header:
            LOG.debug("No AWS trace header found in trace context")
            return None

        return aws_trace_header

    except KeyError as e:
        LOG.warning(f"Missing required field in AWS trace header: {e}")
        return None
    except Exception as e:
        LOG.warning(f"Error extracting AWS trace header: {e}")
        return None


def _get_event_id_from_esm_event(esm_event: dict) -> str | None:
    # SQS source
    if message_id := esm_event.get("messageId"):
        return message_id
    return None


def get_trace_context_from_esm_event(
    esm_event: dict,
    event_storage_service: EventStorageService,
) -> TraceContext:
    if event_id := _get_event_id_from_esm_event(esm_event):
        parent_event = event_storage_service.get_event_by_id(event_id)
        if parent_event:
            parent_id = parent_event.span_id
            trace_id = parent_event.trace_id
            version = parent_event.version
            return TraceContext(
                trace_id=trace_id,
                parent_id=parent_id,
                version=version,
            )
    return TraceContext()
