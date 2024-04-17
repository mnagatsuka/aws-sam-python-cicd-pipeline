import json
import boto3
import logging
import os

# 環境変数設定
LOG_LEVEL = os.environ["LOG_LEVEL"]
QUEUE_URL = os.environ["QUEUE_URL"]

# ロガー設定
logger = logging.getLogger(__name__)
level = logging.getLevelName(LOG_LEVEL)
if not isinstance(level, int):
    # 未設定/設定ミス時のデフォルトのログレベル
    level = logging.WARNING
logger.setLevel(level)

# SQSクライアントクラス
# boto3.client.sqsのラッパークラス
class SQSClient:
    sqs = None

    def __init__(self):
        self.sqs = boto3.client("sqs")

    def send_message(self, *args, **kwargs):
        return self.sqs.send_message(*args, **kwargs)


# SQSクライアントインスタンスを生成
sqs = SQSClient()


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # リクエストボディからデータを取得
    body = json.loads(event["body"])
    id = str(body["id"])
    logger.info(f"id: {id}")
    name = str(body["name"])
    logger.info(f"name: {name}")

    # SQSのメッセージを作成
    message_body = "hello"
    message_attributes = {
        "id": {"StringValue": id, "DataType": "Number"},
        "name": {"StringValue": name, "DataType": "String"},
    }

    try:
        # SQSにメッセージを送信
        response = sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=message_body,
            MessageAttributes=message_attributes,
        )
        logger.info("Message successfully sent to SQS queue.")
        return {
            "statusCode": 200,
            "body": json.dumps("Message successfully sent to SQS queue."),
        }
    except Exception as e:
        logger.error(e)
        return {
            "statusCode": 500,
            "body": json.dumps("An unexpected error occurred."),
        }


if __name__ == "__main__":
    lambda_handler(None, None)
