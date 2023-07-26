import os

from pydantic import BaseModel


class AwsConfig(BaseModel):
    key_id: str
    key: str
    bucket_input: str
    endpoint: str


class RabbitConfig(BaseModel):
    username: str
    password: str
    port: str
    host: str
    parsing_queue: str


class AppConfig(BaseModel):
    temp_file_storage: str
    aws: AwsConfig
    rabbit: RabbitConfig


def load_from_env() -> AppConfig:
    temp_file_storage = os.environ["TEMP_FILE_STORAGE"]
    aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
    aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
    aws_bucket_input = os.environ["AWS_BUCKET_NAME_INPUT"]
    aws_endpoint = os.environ["AWS_ENDPOINT"]
    rabbit_username = os.environ["RABBITMQ_DEFAULT_USER"]
    rabbit_password = os.environ["RABBITMQ_DEFAULT_PASS"]
    rabbit_port = os.environ["RABBIT_PORT"]
    rabbit_host = os.environ["RABBIT_HOST"]
    rabbit_parsing_queue = os.environ["PARSING_QUEUE_NAME"]
    return AppConfig(
        temp_file_storage=temp_file_storage,
        aws=AwsConfig(
            key_id=aws_access_key_id,
            key=aws_secret_access_key,
            bucket_input=aws_bucket_input,
            endpoint=aws_endpoint,
        ),
        rabbit=RabbitConfig(
            username=rabbit_username,
            password=rabbit_password,
            port=rabbit_port,
            host=rabbit_host,
            parsing_queue=rabbit_parsing_queue,
        ),
    )


config = load_from_env()
