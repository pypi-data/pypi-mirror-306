from localstack.utils.aws.arns import parse_arn


def get_queue_url_from_arn(queue_arn: str) -> str:
    parsed_arn = parse_arn(queue_arn)
    account_id = parsed_arn["account"]
    region = parsed_arn["region"]
    resource = parsed_arn["resource"]

    if not all([account_id, region, resource]):
        raise ValueError("Invalid SQS ARN provided")

    return f"https://sqs.{region}.amazonaws.com/{account_id}/{resource}"
