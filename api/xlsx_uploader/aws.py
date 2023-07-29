import boto3
from config import settings

session = boto3.session.Session()

s3_client = session.client(
    service_name="s3",
    endpoint_url=settings.AWS_ENDPOINT,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)


def create_bucket(bucket: str) -> None:
    resp = s3_client.list_buckets()
    existed_buckets = [bucket["Name"] for bucket in resp["Buckets"]]
    if bucket not in existed_buckets:
        s3_client.create_bucket(Bucket=bucket)


def upload_file(file, bucket: str, file_name: str) -> None:
    create_bucket(bucket)
    s3_client.upload_fileobj(file, bucket, file_name)
