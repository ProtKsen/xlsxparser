from django.urls import path

from uploader import views

urlpatterns = [
    path("", views.upload, name="upload_xlsx"),
]
