import pika
from config import settings

credentials = pika.PlainCredentials(settings.RABBITMQ_DEFAULT_USER, settings.RABBITMQ_DEFAULT_PASS)


def publish(queue: str, message: str) -> None:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            settings.RABBIT_HOST, settings.RABBIT_PORT, "/", credentials=credentials
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange="", routing_key=queue, body=message)
    connection.close()
