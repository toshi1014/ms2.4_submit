from django.urls import path
from . import views

urlpatterns = [
    path("", views.campus_list, name = "campus_list")
]