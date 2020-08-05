from django.urls import path
from . import views

urlpatterns = [
    path("", views.faculty_list, name = "faculty_list"),
    path("top_search/<str:prof>/", views.top_search, name = "top_search"),

    path("<str:facul>/", views.lists, name = "list"),
    path("<str:facul>/ranking/", views.ranking, name = "ranking"),
    path("<str:facul>/search/", views.search, name = "search"),
    path("<str:facul>/<str:clas>/", views.clas, name = "class"),
    path("<str:facul>/<str:clas>/<int:pk>/", views.detail, name = "detail"),
    path("<str:facul>/<str:clas>/reply/<int:pk>/", views.reply, name = "reply"),
]

