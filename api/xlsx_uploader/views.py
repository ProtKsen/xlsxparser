import os

from config import settings
from django.contrib import messages
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from pika.exceptions import AMQPError
from xlsx_uploader.forms import UploadFileForm
from xlsx_uploader.rabbit import publish

ALLOWED_EXTENSIONS = set([".xlsx", ".xls"])


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

            file_name = default_storage.save(file.name, file)

            # check filename is queued for parsing
            try:
                publish(settings.PARSING_QUEUE_NAME, file_name)
            except AMQPError:
                messages.add_message(
                    request, messages.ERROR, "Не удалось отправить файл на распознавание"
                )
                return redirect(".")

            return HttpResponse("Файл передан в обработку", status=200)

    form = UploadFileForm()
    return render(request, "upload.html", {"form": form})
