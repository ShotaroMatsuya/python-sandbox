import boto3
import json
import logging
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
s3 = boto3.client("s3")
sts_client = boto3.client("sts")
TABLE_NAME = "S3VirusScanResults"

# ロギング設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def assume_role(account_id):
    """指定されたアカウントの IAM ロールを Assume して一時的な認証情報を取得"""
    role_arn = f"arn:aws:iam::{account_id}:role/GetS3ObjectTagRole"
    
    try:
        response = sts_client.assume_role(
            RoleArn=role_arn, RoleSessionName="GetS3ObjectTagSession"
        )
        credentials = response["Credentials"]

        return boto3.client(
            "s3",
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretAccessKey"],
            aws_session_token=credentials["SessionToken"],
        )
    except ClientError as e:
        logger.error(f"Failed to assume role {role_arn}: {str(e)}")
        raise
      
def get_s3_tags(account_id, bucket_name, object_key):
    """ターゲットアカウントの S3 タグ情報を取得"""
    s3_client = assume_role(account_id)
    
    try:
        tagging = s3_client.get_object_tagging(Bucket=bucket_name, Key=object_key)
        tags = {tag["Key"]: tag["Value"] for tag in tagging.get("TagSet", [])}
        return tags
    except ClientError as e:
        logger.info(f"Can\'t fetching tags for {bucket_name}/{object_key}: {str(e)}")
        return {"scan-status": "NotFound"}

def fetch_all_dynamodb_records():
    """DynamoDB からすべての S3 オブジェクトを取得"""
    table = dynamodb.Table(TABLE_NAME)
    items = []
    last_evaluated_key = None

    while True:
        scan_params = {"Limit": 100} # 100件ずつ処理
        if last_evaluated_key:
            scan_params["ExclusiveStartKey"] = last_evaluated_key

        response = table.scan(**scan_params)
        items.extend(response.get("Items", []))

        last_evaluated_key = response.get("LastEvaluatedKey")
        if not last_evaluated_key:
            break

    return items

def lambda_handler(event, context):
    items = fetch_all_dynamodb_records()
    results = []

    for item in items:
        logger.info(f"Processing item: {json.dumps(item, default=str)}")

        guid = item.get("Guid", "")
        date_scanned = item.get("DateScanned", "")
        bucket_name = item.get("BucketName", "")
        object_key = item.get("Key", "")
        account_id = item.get("AccountId", "")
        region = item.get("Region", "")

        # 各バケットのアカウントに対して Assume Role を実行し、S3 タグを取得
        tags = get_s3_tags(account_id, bucket_name, object_key)
        scan_status = tags.get("scan-status", "NotFound")

        results.append(
            {
                "Guid": guid,
                "DateScanned": date_scanned,
                "BucketName": bucket_name,
                "Key": object_key,
                "ScanResult": scan_status,
                "AccountId": account_id,
                "Region": region,
            }
        )

    logger.info(f"Processed {len(results)} items from DynamoDB.")
    return {"GetS3ObjectTagResult": results}
