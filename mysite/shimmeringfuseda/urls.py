from django.urls import path
from . import views

urlpatterns = [
    path("", views.sf_top, name = "sf_top"),
    path("login/", views.sf_login, name = "sf_login"),
    path("logout/", views.sf_logout, name = "sf_logout"),
    path("<str:key>/control/", views.sf_control, name = "sf_control"),
    path("<str:key>/maintenance/", views.sf_maintenance, name = "sf_maintenace"),
    path("<str:key>/maintenance/mode/<str:state>/", views.sf_maintenance_mode, name = "sf_maintenance_mode"),
    path("<str:key>/control/download/<str:file>", views.sf_download, name = "sf_download"),

    path("<str:key>/control/<str:facul>list/", views.sf_list, name = "sf_list"),
    path("<str:key>/control/<str:facul>/edit", views.sf_edit, name = "sf_edit"),
    path("<str:key>/control/<str:facul>/edit/syllabus", views.sf_syllabus, name = "sf_syllabus"),
]
