import os
import pathlib
import sys
from parser.aws import s3_client
from parser.config import config
from parser.rabbit import channel

import pandas as pd


def download_file(file_name: str, bucket: str):
    if not os.path.exists(f"{config.temp_file_storage}"):
        os.makedirs(f"{config.temp_file_storage}")

    s3_client.download_file(
        Bucket=bucket, Key=file_name, Filename=f"{config.temp_file_storage}/{file_name}"
    )


def delete_file(file_path: str) -> None:
    pathlib.Path(file_path).unlink()


def do_parcing(file_name: str):
    df = pd.read_excel(file_name, sheet_name="Статус")
    df_dict = df.to_dict("records")
    for row in df_dict:
        pass


def callback(ch, method, properties, body):
    file_name = body.decode("utf-8")
    download_file(file_name, config.aws.bucket_input)
    do_parcing(f"{config.temp_file_storage}/{file_name}")
    delete_file(f"{config.temp_file_storage}/{file_name}")


def main():
    channel.basic_consume(
        queue=config.rabbit.parsing_queue, auto_ack=True, on_message_callback=callback
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
