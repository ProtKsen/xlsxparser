import os

from pydantic import BaseModel

from api.config import settings


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
    results_queue: str


class AppConfig(BaseModel):
    temp_file_storage: str
    aws: AwsConfig
    rabbit: RabbitConfig


def get_from_django_settings():
    return AppConfig(
        temp_file_storage="temp",
        aws=AwsConfig(
            key_id=settings.AWS_ACCESS_KEY_ID,
            key=settings.AWS_SECRET_ACCESS_KEY,
            bucket_input=settings.AWS_BUCKET_NAME_INPUT,
            endpoint=settings.AWS_ENDPOINT,
        ),
        rabbit=RabbitConfig(
            username=settings.RABBITMQ_DEFAULT_USER,
            password=settings.RABBITMQ_DEFAULT_PASS,
            port=settings.RABBIT_PORT,
            host=settings.RABBIT_HOST,
            parsing_queue=settings.PARSING_QUEUE_NAME,
            results_queue=settings.RESULTS_QUEUE_NAME,
        ),
    )


config = get_from_django_settings()
