import json
import logging
import os
import re
from pathlib import Path
from typing import Callable, Optional

import aws_cdk as cdk
import pytest
import requests
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from localstack.testing.aws.lambda_utils import _await_event_source_mapping_enabled
from localstack.testing.config import (
    TEST_AWS_ACCOUNT_ID,
    TEST_AWS_REGION_NAME,
)
from localstack.testing.scenario.provisioning import InfraProvisioner
from localstack.testing.snapshots.transformer_utility import (
    SNAPSHOT_BASIC_TRANSFORMER,
    SNAPSHOT_BASIC_TRANSFORMER_NEW,
    TransformerUtility,
)
from localstack.utils import testutil
from localstack.utils.aws.arns import get_partition
from localstack.utils.functions import run_safe
from localstack.utils.strings import short_uid
from localstack.utils.sync import retry, wait_until
from localstack_snapshot.snapshots import SnapshotSession
from localstack_snapshot.snapshots.transformer import RegexTransformer

from eventstudio.api.config import Config
from tests.test_stack.stack import TestStack

LOG = logging.getLogger(__name__)


pytest_plugins = [
    "localstack.testing.pytest.in_memory_localstack",
    "localstack_snapshot.pytest.snapshot",
]

STACK_NAME = "TestStack"

CURRENT_ENV = os.getenv("ENV_FILE", "test.local")
env_path = Config.PACKAGE_ROOT / f".env.{CURRENT_ENV}"

load_dotenv(dotenv_path=env_path)


@pytest.hookimpl()
def pytest_configure(config):
    config.option.start_localstack = True


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    # Remove SQLite after testing
    if os.path.isfile(Config.DATABASE_PATH):
        os.remove(Config.DATABASE_PATH)


@pytest.fixture(scope="session")
def aws_session():
    """
    This fixture returns the Boto Session instance for testing.
    """
    from localstack.testing.aws.util import base_aws_session

    return base_aws_session()


@pytest.fixture(scope="session")
def aws_client_factory(aws_session):
    """
    This fixture returns a client factory for testing.

    Use this fixture if you need to use custom endpoint or Boto config.
    """
    from localstack.testing.aws.util import base_aws_client_factory

    return base_aws_client_factory(aws_session)


@pytest.fixture(scope="session")
def aws_client(aws_client_factory):
    """
    This fixture can be used to obtain Boto clients for testing.

    The clients are configured with the primary testing credentials.
    """
    from localstack.testing.aws.util import base_testing_aws_client

    return base_testing_aws_client(aws_client_factory)


@pytest.fixture(scope="session")
def cdk_template_path():
    return Path(__file__).parent.parent / "cdk_templates"


@pytest.fixture(scope="session")
def infrastructure_setup(cdk_template_path, aws_client):
    def _infrastructure_setup(
        namespace: str, force_synth: Optional[bool] = False
    ) -> InfraProvisioner:
        """
        :param namespace: repo-unique identifier for this CDK app.
            A directory with this name will be created at `tests/aws/cdk_templates/<namespace>/`
        :param force_synth: set to True to always re-synth the CDK app
        :return: an instantiated CDK InfraProvisioner which can be used to deploy a CDK app
        """
        return InfraProvisioner(
            base_path=cdk_template_path,
            aws_client=aws_client,
            namespace=namespace,
            force_synth=force_synth,
            persist_output=True,
        )

    return _infrastructure_setup


@pytest.fixture
def stack_name():
    return STACK_NAME


@pytest.fixture
def event_bridge_infra(infrastructure_setup):
    infra = infrastructure_setup("EventBridge", force_synth=True)

    TestStack(infra.cdk_app, STACK_NAME, env=cdk.Environment())

    with infra.provisioner(skip_teardown=False) as prov:
        yield prov

    # clean up events from database
    requests.delete(Config.get_full_url(Config.ALL_EVENTS))


@pytest.fixture(scope="session")
def account_id():
    return TEST_AWS_ACCOUNT_ID


@pytest.fixture(scope="session")
def region_name():
    return TEST_AWS_REGION_NAME


@pytest.fixture(scope="function")
def snapshot(request, _snapshot_session: SnapshotSession, account_id, region_name):  # noqa: F811
    # Overwrite utility with our own => Will be refactored in the future
    _snapshot_session.transform = TransformerUtility

    _snapshot_session.add_transformer(RegexTransformer(account_id, "1" * 12), priority=2)
    _snapshot_session.add_transformer(RegexTransformer(region_name, "<region>"), priority=2)
    _snapshot_session.add_transformer(
        RegexTransformer(f"arn:{get_partition(region_name)}:", "arn:<partition>:"), priority=2
    )

    # TODO: temporary to migrate to new default transformers.
    #   remove this after all exemptions are gone
    exemptions = [
        "tests/aws/services/acm",
        "tests/aws/services/apigateway",
        "tests/aws/services/cloudwatch",
        "tests/aws/services/cloudformation",
        "tests/aws/services/dynamodb",
        "tests/aws/services/events",
        "tests/aws/services/iam",
        "tests/aws/services/kinesis",
        "tests/aws/services/kms",
        "tests/aws/services/lambda_",
        "tests/aws/services/logs",
        "tests/aws/services/route53",
        "tests/aws/services/route53resolver",
        "tests/aws/services/s3",
        "tests/aws/services/secretsmanager",
        "tests/aws/services/ses",
        "tests/aws/services/sns",
        "tests/aws/services/stepfunctions",
        "tests/aws/services/sqs",
        "tests/aws/services/transcribe",
        "tests/aws/scenario/bookstore",
        "tests/aws/scenario/note_taking",
        "tests/aws/scenario/lambda_destination",
        "tests/aws/scenario/loan_broker",
    ]
    if any(e in request.fspath.dirname for e in exemptions):
        _snapshot_session.add_transformer(SNAPSHOT_BASIC_TRANSFORMER, priority=2)
    else:
        _snapshot_session.add_transformer(SNAPSHOT_BASIC_TRANSFORMER_NEW, priority=2)

    return _snapshot_session


@pytest.fixture
def cleanup_events_in_db():
    def _cleanup_events_in_db():
        requests.delete(Config.get_full_url(Config.ALL_EVENTS))

    yield _cleanup_events_in_db


@pytest.fixture
def wait_for_sqs_messages(aws_client):
    def _wait_for_sqs_messages(queue_url, expected_message_count=1, retries=3, sleep=1):
        def _get_messages():
            messages = aws_client.sqs.receive_message(QueueUrl=queue_url).get("Messages", [])
            assert len(messages) == expected_message_count

        messages = retry(_get_messages, retries=retries, sleep=sleep)
        return messages

    return _wait_for_sqs_messages


@pytest.fixture(autouse=True)
def cleanup_db(cleanup_events_in_db):
    try:
        cleanup_events_in_db()
    except Exception:
        pass
    yield
    try:
        cleanup_events_in_db()
    except Exception:
        pass


@pytest.fixture
def snapshot_with_default_transformers(snapshot):
    snapshot.add_transformers_list(
        [
            snapshot.transform.key_value("creation_time", reference_replacement=False),
            snapshot.transform.key_value("time", reference_replacement=False),
            snapshot.transform.key_value("id", reference_replacement=True),
            snapshot.transform.key_value("event_id", reference_replacement=True),
            snapshot.transform.key_value("trace_id", reference_replacement=True),
            snapshot.transform.key_value("span_id", reference_replacement=True),
            snapshot.transform.key_value("parent_id", reference_replacement=True),
            snapshot.transform.key_value("UnsubscribeURL", reference_replacement=True),
            snapshot.transform.key_value("Signature", reference_replacement=True),
            snapshot.transform.key_value("md5OfBody", reference_replacement=True),
            snapshot.transform.key_value("receiptHandle", reference_replacement=True),
            snapshot.transform.key_value(
                "ApproximateFirstReceiveTimestamp", reference_replacement=False
            ),
            snapshot.transform.key_value("SentTimestamp", reference_replacement=False),
            snapshot.transform.key_value("SigningCertURL", reference_replacement=True),
            snapshot.transform.regex(
                re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"), "<time-string>"
            ),
        ]
    )

    return snapshot


##############
# API Fixtures
##############


@pytest.fixture
def events_url():
    return Config.get_full_url(Config.EVENTS)


@pytest.fixture
def all_events_url():
    return Config.get_full_url(Config.ALL_EVENTS)


#################
# Events Fixtures
#################


@pytest.fixture
def events_create_event_bus(aws_client):
    event_bus_names = []

    def _create_event_bus(**kwargs):
        if "Name" not in kwargs:
            kwargs["Name"] = f"test-event-bus-{short_uid()}"

        response = aws_client.events.create_event_bus(**kwargs)
        event_bus_names.append(kwargs["Name"])
        return response

    yield _create_event_bus

    for event_bus_name in event_bus_names:
        try:
            response = aws_client.events.list_rules(EventBusName=event_bus_name)
            rules = [rule["Name"] for rule in response["Rules"]]

            # Delete all rules for the current event bus
            for rule in rules:
                try:
                    response = aws_client.events.list_targets_by_rule(
                        Rule=rule, EventBusName=event_bus_name
                    )
                    targets = [target["Id"] for target in response["Targets"]]

                    # Remove all targets for the current rule
                    if targets:
                        for target in targets:
                            aws_client.events.remove_targets(
                                Rule=rule, EventBusName=event_bus_name, Ids=[target]
                            )

                    aws_client.events.delete_rule(Name=rule, EventBusName=event_bus_name)
                except Exception as e:
                    LOG.warning(
                        "Failed to delete rule %s: %s",
                        rule,
                        e,
                    )

            # Delete archives for event bus
            event_source_arn = f"arn:aws:events:us-east-1:000000000000:event-bus/{event_bus_name}"
            response = aws_client.events.list_archives(EventSourceArn=event_source_arn)
            archives = [archive["ArchiveName"] for archive in response["Archives"]]
            for archive in archives:
                try:
                    aws_client.events.delete_archive(ArchiveName=archive)
                except Exception as e:
                    LOG.warning(
                        "Failed to delete archive %s: %s",
                        archive,
                        e,
                    )

            aws_client.events.delete_event_bus(Name=event_bus_name)
        except Exception as e:
            LOG.warning(
                "Failed to delete event bus %s: %s",
                event_bus_name,
                e,
            )


@pytest.fixture
def events_put_rule(aws_client):
    rules = []

    def _put_rule(**kwargs):
        if "Name" not in kwargs:
            kwargs["Name"] = f"rule-{short_uid()}"

        response = aws_client.events.put_rule(**kwargs)
        rules.append((kwargs["Name"], kwargs.get("EventBusName", "default")))
        return response

    yield _put_rule

    for rule, event_bus_name in rules:
        try:
            response = aws_client.events.list_targets_by_rule(
                Rule=rule, EventBusName=event_bus_name
            )
            targets = [target["Id"] for target in response["Targets"]]

            # Remove all targets for the current rule
            if targets:
                for target in targets:
                    aws_client.events.remove_targets(
                        Rule=rule, EventBusName=event_bus_name, Ids=[target]
                    )

            aws_client.events.delete_rule(Name=rule, EventBusName=event_bus_name)
        except Exception as e:
            LOG.warning(
                "Failed to delete rule %s: %s",
                rule,
                e,
            )


##############
# SQS Fixtures
##############


@pytest.fixture
def sqs_create_queue(aws_client):
    queue_urls = []

    def factory(**kwargs):
        if "QueueName" not in kwargs:
            kwargs["QueueName"] = "test-queue-%s" % short_uid()

        response = aws_client.sqs.create_queue(**kwargs)
        url = response["QueueUrl"]
        queue_urls.append(url)

        return url

    yield factory

    # cleanup
    for queue_url in queue_urls:
        try:
            aws_client.sqs.delete_queue(QueueUrl=queue_url)
        except Exception as e:
            LOG.debug("error cleaning up queue %s: %s", queue_url, e)


@pytest.fixture
def sqs_queue(sqs_create_queue):
    return sqs_create_queue()


@pytest.fixture
def sqs_get_queue_arn(aws_client) -> Callable:
    def _get_queue_arn(queue_url: str) -> str:
        return aws_client.sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=["QueueArn"])[
            "Attributes"
        ]["QueueArn"]

    return _get_queue_arn


@pytest.fixture
def sqs_allow_events_to_send_messages(aws_client):
    def _sqs_allow_events_to_send_messages(queue_arn, queue_url):
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "AllowEventBridge",
                    "Effect": "Allow",
                    "Principal": {"Service": "events.amazonaws.com"},
                    "Action": "sqs:SendMessage",
                    "Resource": queue_arn,
                }
            ],
        }
        aws_client.sqs.set_queue_attributes(
            QueueUrl=queue_url, Attributes={"Policy": json.dumps(policy)}
        )

    yield _sqs_allow_events_to_send_messages


##############
# SNS Fixtures
##############


@pytest.fixture
def sns_create_topic(aws_client):
    topic_arns = []

    def _create_topic(**kwargs):
        if "Name" not in kwargs:
            kwargs["Name"] = "test-topic-%s" % short_uid()
        response = aws_client.sns.create_topic(**kwargs)
        topic_arns.append(response["TopicArn"])
        return response

    yield _create_topic

    for topic_arn in topic_arns:
        try:
            aws_client.sns.delete_topic(TopicArn=topic_arn)
        except Exception as e:
            LOG.debug("error cleaning up topic %s: %s", topic_arn, e)


@pytest.fixture
def sns_subscription(aws_client):
    sub_arns = []

    def _create_sub(**kwargs):
        if kwargs.get("ReturnSubscriptionArn") is None:
            kwargs["ReturnSubscriptionArn"] = True

        # requires 'TopicArn', 'Protocol', and 'Endpoint'
        response = aws_client.sns.subscribe(**kwargs)
        sub_arn = response["SubscriptionArn"]
        sub_arns.append(sub_arn)
        return response

    yield _create_sub

    for sub_arn in sub_arns:
        try:
            aws_client.sns.unsubscribe(SubscriptionArn=sub_arn)
        except Exception as e:
            LOG.debug("error cleaning up subscription %s: %s", sub_arn, e)


@pytest.fixture
def sns_allow_topic_sqs_queue(aws_client):
    def _allow_sns_topic(sqs_queue_url, sqs_queue_arn, sns_topic_arn) -> None:
        # allow topic to write to sqs queue
        aws_client.sqs.set_queue_attributes(
            QueueUrl=sqs_queue_url,
            Attributes={
                "Policy": json.dumps(
                    {
                        "Statement": [
                            {
                                "Effect": "Allow",
                                "Principal": {"Service": "sns.amazonaws.com"},
                                "Action": "sqs:SendMessage",
                                "Resource": sqs_queue_arn,
                                "Condition": {"ArnEquals": {"aws:SourceArn": sns_topic_arn}},
                            }
                        ]
                    }
                )
            },
        )

    return _allow_sns_topic


@pytest.fixture
def sns_policy(aws_client):
    def _add_policy(topic_arn):
        policy = {
            "Version": "2012-10-17",
            "Id": f"sns-eventbridge-{short_uid()}",
            "Statement": [
                {
                    "Sid": f"SendMessage-{short_uid()}",
                    "Effect": "Allow",
                    "Principal": {"Service": "events.amazonaws.com"},
                    "Action": "sns:Publish",
                    "Resource": topic_arn,
                }
            ],
        }
        aws_client.sns.set_topic_attributes(
            TopicArn=topic_arn, AttributeName="Policy", AttributeValue=json.dumps(policy)
        )

    yield _add_policy


#################
# Lambda Fixtures
#################


@pytest.fixture
def wait_until_lambda_ready(aws_client):
    def _wait_until_ready(function_name: str, qualifier: str = None, client=None):
        client = client or aws_client.lambda_

        def _is_not_pending():
            kwargs = {}
            if qualifier:
                kwargs["Qualifier"] = qualifier
            try:
                result = (
                    client.get_function(FunctionName=function_name)["Configuration"]["State"]
                    != "Pending"
                )
                LOG.debug("lambda state result: result=%s", result)
                return result
            except Exception as e:
                LOG.error(e)
                raise

        wait_until(_is_not_pending)

    return _wait_until_ready


role_assume_policy = """
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
""".strip()

role_policy_su = {
    "Version": "2012-10-17",
    "Statement": [{"Effect": "Allow", "Action": ["*"], "Resource": ["*"]}],
}


@pytest.fixture(scope="session")
def lambda_su_role(aws_client):
    role_name = f"lambda-autogenerated-{short_uid()}"
    role = aws_client.iam.create_role(
        RoleName=role_name, AssumeRolePolicyDocument=role_assume_policy
    )["Role"]
    policy_name = f"lambda-autogenerated-{short_uid()}"
    policy_arn = aws_client.iam.create_policy(
        PolicyName=policy_name, PolicyDocument=json.dumps(role_policy_su)
    )["Policy"]["Arn"]
    aws_client.iam.attach_role_policy(RoleName=role_name, PolicyArn=policy_arn)

    yield role["Arn"]

    paginator = aws_client.iam.get_paginator("list_attached_role_policies")
    for page in paginator.paginate(RoleName=role_name):
        if page["AttachedPolicies"]:
            attached_policy_arns = [p["PolicyArn"] for p in page["AttachedPolicies"]]
            for policy_arn in attached_policy_arns:
                run_safe(
                    aws_client.iam.detach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
                )
                run_safe(aws_client.iam.delete_policy(PolicyArn=policy_arn))

    run_safe(aws_client.iam.delete_role(RoleName=role_name))


@pytest.fixture
def create_lambda_function(aws_client, wait_until_lambda_ready, lambda_su_role):
    lambda_arns_and_clients = []
    log_groups = []
    lambda_client = aws_client.lambda_
    logs_client = aws_client.logs
    s3_client = aws_client.s3

    def _create_lambda_function(*args, **kwargs):
        client = kwargs.get("client") or lambda_client
        kwargs["client"] = client
        kwargs["s3_client"] = s3_client
        func_name = kwargs.get("func_name")
        assert func_name
        del kwargs["func_name"]

        if not kwargs.get("role"):
            kwargs["role"] = lambda_su_role

        def _create_function():
            resp = testutil.create_lambda_function(func_name, **kwargs)
            lambda_arns_and_clients.append((resp["CreateFunctionResponse"]["FunctionArn"], client))
            wait_until_lambda_ready(function_name=func_name, client=client)
            log_group_name = f"/aws/lambda/{func_name}"
            log_groups.append(log_group_name)
            return resp

        # @AWS, takes about 10s until the role/policy is "active", until then it will fail
        # localstack should normally not require the retries and will just continue here
        return retry(_create_function, retries=3, sleep=4)

    yield _create_lambda_function

    for arn, client in lambda_arns_and_clients:
        try:
            client.delete_function(FunctionName=arn)
        except Exception:
            LOG.debug("Unable to delete function arn=%s in cleanup", arn)

    for log_group_name in log_groups:
        try:
            logs_client.delete_log_group(logGroupName=log_group_name)
        except Exception:
            LOG.debug("Unable to delete log group %s in cleanup", log_group_name)


@pytest.fixture
def create_event_source_mapping(aws_client):
    uuids = []

    def _create_event_source_mapping(*args, **kwargs):
        response = aws_client.lambda_.create_event_source_mapping(*args, **kwargs)
        mapping_uuid = response["UUID"]
        uuids.append(mapping_uuid)
        _await_event_source_mapping_enabled(aws_client.lambda_, mapping_uuid)

        return response

    yield _create_event_source_mapping

    for uuid in uuids:
        try:
            aws_client.lambda_.delete_event_source_mapping(UUID=uuid)
        except Exception:
            LOG.debug("Unable to delete event source mapping %s in cleanup", uuid)


#############
# S3 Fixtures
#############


@pytest.fixture
def s3_empty_bucket(aws_client):
    """
    Returns a factory that given a bucket name, deletes all objects and deletes all object versions
    """

    # Boto resource would make this a straightforward task, but our internal client does not support Boto resource
    # FIXME: this won't work when bucket has more than 1000 objects
    def factory(bucket_name: str):
        kwargs = {}
        try:
            aws_client.s3.get_object_lock_configuration(Bucket=bucket_name)
            kwargs["BypassGovernanceRetention"] = True
        except ClientError:
            pass

        response = aws_client.s3.list_objects_v2(Bucket=bucket_name)
        objects = [{"Key": obj["Key"]} for obj in response.get("Contents", [])]
        if objects:
            aws_client.s3.delete_objects(
                Bucket=bucket_name,
                Delete={"Objects": objects},
                **kwargs,
            )

        response = aws_client.s3.list_object_versions(Bucket=bucket_name)
        versions = response.get("Versions", [])
        versions.extend(response.get("DeleteMarkers", []))

        object_versions = [{"Key": obj["Key"], "VersionId": obj["VersionId"]} for obj in versions]
        if object_versions:
            aws_client.s3.delete_objects(
                Bucket=bucket_name,
                Delete={"Objects": object_versions},
                **kwargs,
            )

    yield factory


@pytest.fixture
def s3_create_bucket(s3_empty_bucket, aws_client):
    buckets = []

    def factory(**kwargs) -> str:
        if "Bucket" not in kwargs:
            kwargs["Bucket"] = "test-bucket-%s" % short_uid()

        if (
            "CreateBucketConfiguration" not in kwargs
            and aws_client.s3.meta.region_name != "us-east-1"
        ):
            kwargs["CreateBucketConfiguration"] = {
                "LocationConstraint": aws_client.s3.meta.region_name
            }

        aws_client.s3.create_bucket(**kwargs)
        buckets.append(kwargs["Bucket"])
        return kwargs["Bucket"]

    yield factory

    # cleanup
    for bucket in buckets:
        try:
            s3_empty_bucket(bucket)
            aws_client.s3.delete_bucket(Bucket=bucket)
        except Exception as e:
            LOG.debug("error cleaning up bucket %s: %s", bucket, e)
