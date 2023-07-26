from django.urls import path
from xlsx_uploader import views

urlpatterns = [
    path("", views.upload, name="upload_xlsx"),
]
