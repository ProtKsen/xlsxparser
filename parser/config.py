from pydantic import BaseModel

from api.config import settings


class RabbitConfig(BaseModel):
    username: str
    password: str
    port: str
    host: str
    parsing_queue: str
    results_queue: str


class AppConfig(BaseModel):
    rabbit: RabbitConfig


def get_from_django_settings():
    return AppConfig(
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
