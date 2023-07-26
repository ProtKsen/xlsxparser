import pika
from config import config

credentials = pika.PlainCredentials(config.rabbit.username, config.rabbit.password)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(config.rabbit.host, config.rabbit.port, "/", credentials=credentials)
)
channel = connection.channel()
channel.queue_declare(queue=config.rabbit.parsing_queue)
