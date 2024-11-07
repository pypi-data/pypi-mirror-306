import json
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from typing import Callable

from localstack.aws.api import RequestContext

from eventstudio.api.types.trace_context import TraceContext
from eventstudio.constants import INTERNAL_REQUEST_TRACE_HEADER

LOG = logging.getLogger(__name__)


thread_local_tracing = threading.local()


def extract_trace_context_from_context(context: RequestContext) -> TraceContext:
    trace_context = TraceContext()
    for item in context.request.headers:
        if item[0] == INTERNAL_REQUEST_TRACE_HEADER:
            trace_context = TraceContext(**json.loads(item[1]))
            break
    return trace_context


def get_trace_context() -> TraceContext:
    try:
        return getattr(thread_local_tracing, "trace_context", None) or TraceContext()
    except AttributeError:
        return TraceContext()


def set_trace_context(trace_context: TraceContext):
    thread_local_tracing.trace_context = trace_context


def wrap_function_with_context(fn: Callable, trace_context: TraceContext) -> Callable:
    """Wrap a function to restore the captured context before execution."""

    @wraps(fn)
    def context_preserving_fn(*args, **kwargs):
        # Restore the captured context in the worker thread
        set_trace_context(trace_context)

        return fn(*args, **kwargs)

    return context_preserving_fn


def submit_with_trace_context(executor: ThreadPoolExecutor, fn: Callable, /, *args, **kwargs):
    """Submit a function to the executor while preserving threading.local context."""
    trace_context = get_trace_context()
    wrapped_fn = wrap_function_with_context(fn, trace_context)

    return executor.submit(wrapped_fn, *args, **kwargs)
