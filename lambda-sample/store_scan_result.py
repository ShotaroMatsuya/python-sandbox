import json
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")
DYNAMODB_TABLE_NAME = "S3VirusScanResults"

def get_scan_attempts(guid, date_scanned):
    """DynamoDBから現在のReScanAttemptedを取得"""
    try:
        table = dynamodb.Table(DYNAMODB_TABLE_NAME)
        response = table.get_item(Key={"Guid": guid, "DateScanned": date_scanned})
        if "Item" in response:
            return response["Item"].get("ReScanAttempted", 0)
        return 0
    except Exception as e:
        logger.error(f"Failed to fetch ReScanAttempted count: {str(e)}")
        return 0

def store_scan_result(
    guid,
    date_scanned,
    account_id,
    bucket_name,
    file_key,
    scan_result,
    file_size,
    region,
    scan_results,
    file_exists,
    rescan_attempted
):
    """DynamoDBにスキャン結果を保存する"""
    try:
        table = dynamodb.Table(DYNAMODB_TABLE_NAME)
        item = {
            "Guid": guid,
            "DateScanned": date_scanned,
            "AccountId": account_id,
            "BucketName": bucket_name,
            "FileExists": file_exists,
            "FileSize": int(file_size),
            "Key": file_key,
            "Region": region,
            "Result": scan_result,
            "ScanResults": scan_results,
            "ReScanAttempted": rescan_attempted,
        }
        
        response = table.put_item(Item=item)
        logger.info(f"Stored scan result in DynamoDB: {response}")
    except Exception as e:
        logger.error(f"Failed to store scan result in DynamoDB: {str(e)}")

def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))
    try:
        message_str = event["detail"].get("Message", "{}")
        message = json.loads(message_str)

        bucket_name = message.get("bucketName", "N/A")
        file_key = message.get("key", "N/A")
        guid = message.get("guid", "N/A")
        date_scanned = message.get("dateScanned", "N/A")
        account_id = message.get("accountId", "N/A")
        scan_result = message.get("result", "N/A")
        file_size = message.get("fileSize", 0)
        region = message.get("region", "N/A")
        scan_results = message.get("scanResults", [])
        file_exists = message.get("fileExists", False)
        rescan_attempted = get_scan_attempts(guid, date_scanned)

        # スキャン結果をDynamoDBに保存
        scan_action = "" # 空文字で初期化
        if scan_result == "Error":
            scan_action = "rescan"
            rescan_attempted += 1
        store_scan_result(
            guid,
            date_scanned,
            account_id,
            bucket_name,
            file_key,
            scan_result,
            file_size,
            region,
            scan_results,
            file_exists,
            rescan_attempted,
        )

        return {
            "statusCode": 200,
            "body": "Scan result stored successfully",
            "scanAction": scan_action,
            "ReScanAttempted": rescan_attempted,
        }
    except Exception as e:
        logger.error(f"Error processing event: {e}")
        raise
