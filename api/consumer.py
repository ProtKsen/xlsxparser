import json
import os
import sys

import django
import pika
import requests
from config import settings
from django.urls import reverse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


def callback(ch, method, properties, body):
    data = json.loads(body)
    host = os.environ["APP_HOST"]
    port = os.environ["APP_PORT"]
    url = f'http://{host}:{port}{reverse("add_billboard")}'
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url=url, data=json.dumps(data), headers=headers)
    print(resp)


def main():
    credentials = pika.PlainCredentials(
        settings.RABBITMQ_DEFAULT_USER, settings.RABBITMQ_DEFAULT_PASS
    )

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            settings.RABBIT_HOST,
            settings.RABBIT_PORT,
            "/",
            credentials=credentials,
        )
    )

    channel = connection.channel()
    channel.queue_declare(queue=settings.RESULTS_QUEUE_NAME)

    channel.basic_consume(
        queue=settings.RESULTS_QUEUE_NAME, on_message_callback=callback, auto_ack=True
    )

    print("Started Consuming...")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
