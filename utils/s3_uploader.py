import boto3
from botocore.exceptions import ClientError, BotoCoreError

s3_client = boto3.client("s3", region_name="us-east-1")

def upload_file(bucket: str, key: str, content: bytes ) -> str:
    try:
        s3_client.put_object(Bucket=bucket, Key=key, Body=content)
        return f"s3://{bucket}/{key}"
    except (ClientError, BotoCoreError) as e:
        raise RuntimeError(f"Error uploading file to S3: {str(e)}")

def list_objects(bucket: str, prefix: str = "") -> list[str]:
    try:
        response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        return [obj["Key"] for obj in response.get("Contents", [])]
    except (ClientError, BotoCoreError) as e:
        raise RuntimeError(f"Error listing objects in S3: {str(e)}")