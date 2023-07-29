from parser.config import config

import pika

credentials = pika.PlainCredentials(config.rabbit.username, config.rabbit.password)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(config.rabbit.host, config.rabbit.port, "/", credentials=credentials)
)
channel = connection.channel()
channel.queue_declare(queue=config.rabbit.parsing_queue, durable=True)


def publish(queue: str, message: str) -> None:
    channel.basic_publish(exchange="", routing_key=queue, body=message)
