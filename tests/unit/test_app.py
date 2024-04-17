import pytest
import logging
import json
from src.app import (
    SQSClient,
    lambda_handler,
)

# テストデータ
# lambda_handler
test_lambda_handler_params = {
    "1_success_send_message": (
        # test_id
        "1_success_send_message",
        # condition
        {
            "event": {
                "body": {"id": 1234, "name": "xxx"},
            },
            "context": None,
        },
        # response
        {
            "sqs": {
                "send_message": {
                    "MD5OfMessageBody": "test",
                    "MessageId": "1",
                }
            }
        },
        # side_effect
        {"sqs": {"send_message": None}},
        # expected
        {
            "statusCode": 200,
            "body": "Message successfully sent to SQS queue.",
            "func_name": "src.app",
            "log_level": 20,  # INFO
            "log_message": ["Message successfully sent to SQS queue."],
        },
    ),
    "2_fail_send_message": (
        # test_id
        "2_fail_send_message",
        # condition
        {
            "event": {
                "body": {"id": 1234, "name": "xxx"},
            },
            "context": None,
        },
        # response
        {
            "sqs": {
                "send_message": {
                    "MD5OfMessageBody": "test",
                    "MessageId": "1",
                }
            }
        },
        # side_effect
        {"sqs": {"send_message": Exception("An unexpected error occurred.")}},
        # expected
        {
            "statusCode": 500,
            "body": "An unexpected error occurred.",
            "func_name": "src.app",
            "log_level": 40,  # ERROR
            "log_message": ["An unexpected error occurred."],
        },
    ),
    "3_export_info_log": (
        # test_id
        "3_export_info_log",
        # condition
        {
            "event": {
                "body": {"id": 1234, "name": "xxx"},
            },
            "context": None,
        },
        # response
        {
            "sqs": {
                "send_message": {
                    "MD5OfMessageBody": "test",
                    "MessageId": "1",
                }
            }
        },
        # side_effect
        {"sqs": {"send_message": None}},
        # expected
        {
            "statusCode": 200,
            "body": "Message successfully sent to SQS queue.",
            "func_name": "src.app",
            "log_level": 20,  # INFO
            "log_message": [
                "id: 1234",
                "name: 'xxx'",
                "Message successfully sent to SQS queue.",
            ],
        },
    ),
}

# テストメソッド
@pytest.mark.parametrize(
    "test_id, condition, response, side_effect, expected",
    list(test_lambda_handler_params.values()),
    ids=list(test_lambda_handler_params.keys()),
)
def test_lambda_handler(
    mocker,
    caplog,
    test_id,
    condition,
    response,
    side_effect,
    expected,
):
    # given
    caplog.set_level(logging.INFO)

    # SQSへのメッセージ送信メソッドのモックを生成
    mock_send_message = mocker.patch.object(
        SQSClient,
        "send_message",
        return_value=response["sqs"]["send_message"],
        side_effect=side_effect["sqs"]["send_message"],
    )

    # テストデータオブジェクトをJSON形式に変換する
    condition["event"]["body"] = json.dumps(condition["event"]["body"])

    # then
    # Lambda関数を実行
    response = lambda_handler(condition["event"], condition["context"])

    # 実行結果を判定
    assert response["statusCode"] == expected["statusCode"]
    assert response["body"] == json.dumps(expected["body"])
    for message in expected["log_message"]:
        assert (
            expected["func_name"],
            expected["log_level"],
            message,
        ) in caplog.record_tuples
