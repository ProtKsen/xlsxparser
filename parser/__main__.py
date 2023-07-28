import os
import pathlib
import sys
from parser.aws import download_file
from parser.config import config
from parser.parser import do_parcing
from parser.rabbit import channel


def delete_file(file_path: str) -> None:
    pathlib.Path(file_path).unlink()


def callback(ch, method, properties, body):
    file_name = body.decode("utf-8")
    download_file(file_name, config.aws.bucket_input)
    file_path = f"{config.temp_file_storage}/{file_name}"
    do_parcing(file_path)
    delete_file(file_path)
    channel.close()


def main():
    channel.basic_consume(
        queue=config.rabbit.parsing_queue, on_message_callback=callback, auto_ack=True
    )
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
