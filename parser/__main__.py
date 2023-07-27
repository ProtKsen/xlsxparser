import json
import os
import pathlib
import sys
from parser.aws import download_file
from parser.config import config
from parser.rabbit import channel, publish

import pandas as pd


def delete_file(file_path: str) -> None:
    pathlib.Path(file_path).unlink()


def do_parcing(file_name: str):
    df = pd.read_excel(file_name, sheet_name="Статус")
    df_dict = df.to_dict("records")
    for row in df_dict:
        publish(config.rabbit.results_queue, json.dumps(row))


def callback(ch, method, properties, body):
    file_name = body.decode("utf-8")
    download_file(file_name, config.aws.bucket_input)
    do_parcing(f"{config.temp_file_storage}/{file_name}")
    delete_file(f"{config.temp_file_storage}/{file_name}")


def main():
    channel.basic_consume(queue=config.rabbit.parsing_queue, on_message_callback=callback)
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
