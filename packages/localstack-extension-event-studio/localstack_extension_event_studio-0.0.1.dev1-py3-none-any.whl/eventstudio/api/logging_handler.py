import json
import logging
from typing import Set

from localstack.aws.api import RequestContext
from localstack.pro.core.services.iam.policy_engine.engine import EvaluationCallback
from localstack.pro.core.services.iam.policy_engine.models import PolicyEvaluationResult

from eventstudio.api.event_storage import EventStorageService
from eventstudio.api.types.errors import ErrorType, InputErrorModel
from eventstudio.api.utils.tracing_utils import (
    extract_trace_context_from_context,
    get_trace_context,
)

LOG = logging.getLogger(__name__)
LOG_MESSAGES_TO_CAPTURE: Set[str] = {
    "InvalidArgument",
    "ResourceNotFoundException at get_event_bus",
    "InternalInfoEvents at iterate over targets",
    "InternalException at process_entries",
    "InternalInfoEvents at process_rules",
    "InternalInfoEvents at matches_rule",
}


class EventStudioLogHandler(logging.Handler):
    def __init__(self, event_studio_service: EventStorageService) -> None:
        logging.Handler.__init__(self=self)
        self._event_studio_service = event_studio_service

    def emit(self, record: logging.LogRecord) -> None:
        if record.levelno >= logging.ERROR:
            self._process_log_error(record)
        elif any(msg in record.getMessage() for msg in LOG_MESSAGES_TO_CAPTURE):
            self._process_log_error(record)

    def _process_log_error(self, record: logging.LogRecord) -> None:
        trace_context = get_trace_context()
        if trace_context.parent_id is not None:
            self._create_error_record(record, trace_context.parent_id)

    def _create_error_record(self, record: logging.LogRecord, span_id: str) -> None:
        message = record.getMessage()
        try:
            message_dict = json.loads(message)
            if "ErrorCode" in message_dict.keys():
                error_type = ErrorType.LOCALSTACK_ERROR
                code = message_dict["ErrorCode"]
                message = message_dict["ErrorMessage"]
            elif "InfoCode" in message_dict.keys():
                error_type = ErrorType.LOCALSTACK_WARNING
                code = message_dict["InfoCode"]
                message = message_dict["InfoMessage"]
            message = f"{code}: {message}"

        except json.JSONDecodeError:
            error_type = ErrorType.LOCALSTACK_ERROR

        error_record = InputErrorModel(
            span_id=span_id,
            error_message=message,
            error_type=error_type,
        )
        self._event_studio_service.add_error(InputErrorModel.model_validate(error_record))


class EventStudioBasicLogHandler(logging.Handler):
    def __init__(self, event_studio_service: EventStorageService) -> None:
        logging.Handler.__init__(self=self)
        self._event_studio_service = event_studio_service

    def emit(self, record) -> None:
        trace_context = get_trace_context()
        if trace_context.parent_id is None:
            return

        error_record = InputErrorModel(
            span_id=trace_context.parent_id,
            error_message=record.msg,
            error_type=ErrorType.LOCALSTACK_ERROR,
        )
        self._event_studio_service.add_error(error_record)


class EventStudioIAMCallback(EvaluationCallback):
    def __init__(self, event_studio_service: EventStorageService) -> None:
        self._event_studio_service: EventStorageService = event_studio_service

    def __call__(self, evaluation_result: PolicyEvaluationResult, context: RequestContext):
        if evaluation_result.allowed:
            return

        trace_context = extract_trace_context_from_context(context)
        if trace_context.parent_id is None:
            return

        error_message = "Request for service '{}' for operation '{}' denied.".format(
            context.service.service_id, context.service_operation.operation
        )
        necessary_permissions = "Necessary permissions for this action: {}".format(
            [
                f"Action '{result.action}' for '{result.resource}'"
                for result in evaluation_result.explicit_deny
                + evaluation_result.explicit_allow
                + evaluation_result.implicit_deny
            ]
        )
        explicitly_denied_permissions = "{} permissions have been explicitly denied: {}".format(
            len(evaluation_result.explicit_deny),
            [
                f"Action '{result.action}' for '{result.resource}'"
                for result in evaluation_result.explicit_deny
            ],
        )
        explicitly_allowed_permissions = "{} permissions have been explicitly allowed: {}".format(
            len(evaluation_result.explicit_allow),
            [
                f"Action '{result.action}' for '{result.resource}'"
                for result in evaluation_result.explicit_allow
            ],
        )
        implicitly_denied_permissions = "{} permissions have been implicitly denied: {}".format(
            len(evaluation_result.implicit_deny),
            [
                f"Action '{result.action}' for '{result.resource}'"
                for result in evaluation_result.implicit_deny
            ],
        )
        error_object = {
            "error_message": error_message,
            "necessary_permissions": necessary_permissions,
            "explicitly_denied_permissions": explicitly_denied_permissions,
            "explicitly_allowed_permissions": explicitly_allowed_permissions,
            "implicitly_denied_permissions": implicitly_denied_permissions,
        }

        error_record = InputErrorModel(
            span_id=trace_context.parent_id,
            error_message=json.dumps(error_object),
            error_type=ErrorType.IAM_ERROR,
        )
        self._event_studio_service.add_error(error_record)
