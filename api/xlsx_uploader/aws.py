import boto3
from botocore.exceptions import ClientError
from config import settings
from rest_framework.exceptions import APIException


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = "Faild to save file"
    default_code = "service_unavailable"


session = boto3.session.Session()

s3_client = session.client(
    service_name="s3",
    endpoint_url=settings.AWS_ENDPOINT,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)


class AWSRepo:
    name = "file"

    def create_bucket(self, bucket: str) -> None:
        resp = s3_client.list_buckets()
        existed_buckets = [bucket["Name"] for bucket in resp["Buckets"]]
        if bucket not in existed_buckets:
            s3_client.create_bucket(Bucket=bucket)

    def upload_file_to_bucket(self, file, bucket_input: str, filename: str) -> None:
        try:
            s3_client.upload_fileobj(file, bucket_input, filename)
        except ClientError:
            raise ServiceUnavailable
