import os
from parser.config import config

import boto3

session = boto3.session.Session()

s3_client = session.client(
    service_name="s3",
    endpoint_url=config.aws.endpoint,
    aws_access_key_id=config.aws.key_id,
    aws_secret_access_key=config.aws.key,
)


def download_file(file_name: str, bucket: str):
    if not os.path.exists(f"{config.temp_file_storage}"):
        os.makedirs(f"{config.temp_file_storage}")

    s3_client.download_file(
        Bucket=bucket, Key=file_name, Filename=f"{config.temp_file_storage}/{file_name}"
    )
