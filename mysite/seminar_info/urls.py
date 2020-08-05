from django.urls import path
from . import views

urlpatterns = [
    path("", views.se_faculty_list, name = "se_faculty_list")
]