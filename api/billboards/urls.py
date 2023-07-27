from billboards import views
from django.urls import path

urlpatterns = [
    path("add", views.add, name="add_billboard"),
]
