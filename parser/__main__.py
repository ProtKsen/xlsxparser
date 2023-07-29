import os
import pathlib
import sys
from parser.config import config
from parser.parser import do_parcing
from parser.rabbit import channel


def delete_file(file_path: str) -> None:
    pathlib.Path(file_path).unlink()


def callback(ch, method, properties, body):
    file_name = body.decode("utf-8")
    file_path = f"api/media/{file_name}"
    do_parcing(file_path)
    delete_file(file_path)
    print("Parsing finished!")


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
