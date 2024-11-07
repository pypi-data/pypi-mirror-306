import json
import os


def handler(event, context):
    # Print the trace header from the Lambda environment
    trace_header = os.getenv("_X_AMZN_TRACE_ID", "No trace header found")
    print(f"Lambda received trace header: {trace_header}")

    # Process messages
    for record in event["Records"]:
        print(f"Processing message: {record['messageId']}")
        message = json.loads(record["body"])
        print(f"Message content: {message}")

    return {"statusCode": 200, "body": json.dumps("Messages processed successfully")}
