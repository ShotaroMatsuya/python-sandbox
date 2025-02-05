import json
import logging
import boto3
from datadog_lambda.metric import lambda_metric
from datadog_lambda.wrapper import datadog_lambda_wrapper

dynamodb = boto3.resource("dynamodb")
DYNAMODB_TABLE_NAME = "S3VirusScanResults"

# ロギング設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)


@datadog_lambda_wrapper
def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event, default=str)}")

    guid = event.get("Guid", "")
    date_scanned = event.get("DateScanned", "")
    bucket_name = event.get("BucketName", "")
    object_key = event.get("Key", "")
    scan_result = event.get("ScanResult", "")
    account_id = event.get("AccountId", "")

    metric_value = 1.00 if scan_result in ["Infected", "Error", "Unscannable"] else 0.00

    send_metric_to_datadog(scan_result, metric_value, bucket_name, object_key, account_id)

    # `NotFound` / `Clean` の場合は DynamoDB からレコード削除
    if scan_result in ["NotFound", "Clean"]:
        delete_from_dynamodb(guid, date_scanned)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Metrics sent to Datadog and cleanup processed"}),
    }


def send_metric_to_datadog(scan_result, metric_value, bucket_name, object_key, account_id):
    """Datadog にカスタムメトリクスを送信"""
    try:
        lambda_metric(
            "s3.virus_scan.result",
            value=metric_value,
            tags=[
                f"scan_result:{scan_result.lower()}",
                f"s3_account_id:{account_id}",
                f"bucket_name:{bucket_name}",
                f"file_key:{object_key}",
            ],
        )
        logger.info(
            f"Sent metric to Datadog: scan_result={scan_result}, value={metric_value}"
        )
    except Exception as e:
        logger.error(f"Failed to send metric to Datadog: {str(e)}")


def delete_from_dynamodb(guid, date_scanned):
    """DynamoDB から該当オブジェクトを削除"""
    try:
        table = dynamodb.Table(DYNAMODB_TABLE_NAME)
        delete_key = {"Guid": guid, "DateScanned": date_scanned}
        response = table.delete_item(Key=delete_key)
        logger.info(f"DynamoDB entry deleted: {delete_key}")
    except Exception as e:
        logger.error(f"Failed to delete entry {delete_key} from DynamoDB: {str(e)}")
