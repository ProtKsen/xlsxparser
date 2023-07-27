"""
URL configuration for src project.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("xlsx_uploader.urls")),
    path("billboard/", include("billboards.urls")),
]
