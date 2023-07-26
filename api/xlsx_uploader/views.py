import os

import pika
from config import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from rest_framework.exceptions import UnsupportedMediaType
from xlsx_uploader.aws import AWSRepo
from xlsx_uploader.forms import UploadFileForm

ALLOWED_EXTENSIONS = set([".xlsx", ".xls"])

bucket = settings.AWS_BUCKET_NAME_INPUT
aws_repo = AWSRepo()


@require_http_methods(["GET", "POST"])
def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]

            file_extension = os.path.splitext(file.name)[-1]
            if file_extension.lower() not in ALLOWED_EXTENSIONS:
                raise UnsupportedMediaType

            aws_repo.create_bucket(bucket)
            aws_repo.upload_file_to_bucket(file, bucket, file.name)

            credentials = pika.PlainCredentials("morok", "pass")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters("localhost", 5672, "/", credentials=credentials)
            )
            channel = connection.channel()
            channel.queue_declare(queue="files for parsing")
            channel.basic_publish(
                exchange="", routing_key="files for parsing", body=f"{file.name}"
            )
            connection.close()

            return HttpResponse({"file": file.name}, status=201)

    form = UploadFileForm()
    context = {"form": form}
    return render(request, "upload.html", context)
