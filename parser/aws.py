from parser.config import config

import boto3

session = boto3.session.Session()

s3_client = session.client(
    service_name="s3",
    endpoint_url=config.aws.endpoint,
    aws_access_key_id=config.aws.key_id,
    aws_secret_access_key=config.aws.key,
)
