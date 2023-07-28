import os

from botocore.exceptions import ClientError, EndpointConnectionError
from config import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from pika.exceptions import AMQPError
from xlsx_uploader.aws import upload_file
from xlsx_uploader.forms import UploadFileForm
from xlsx_uploader.rabbit import publish

ALLOWED_EXTENSIONS = set([".xlsx", ".xls"])

bucket = settings.AWS_BUCKET_NAME_INPUT


@require_http_methods(["GET", "POST"])
def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES["file"]

            # check file extension
            file_extension = os.path.splitext(file.name)[-1]
            if file_extension.lower() not in ALLOWED_EXTENSIONS:
                messages.add_message(request, messages.ERROR, "Неверный формат файла")
                return redirect(".")

            # check file is saved in storage
            try:
                upload_file(file, bucket, file.name)
            except (ClientError, EndpointConnectionError):
                messages.add_message(request, messages.ERROR, "Не удалось сохранить файл")
                return redirect(".")

            # check filename is queued for parsing
            try:
                publish(settings.PARSING_QUEUE_NAME, file.name)
            except AMQPError:
                messages.add_message(
                    request, messages.ERROR, "Не удалось отправить файл на распознавание"
                )
                return redirect(".")

            return HttpResponse("Файл передан в обработку", status=200)

    form = UploadFileForm()
    return render(request, "upload.html", {"form": form})
