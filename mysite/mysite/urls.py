from django.contrib import admin
from django.urls import path, include
from . import views
import mysite

urlpatterns = [
    path('admin/', admin.site.urls),

    path("", mysite.views.top, name = "top"),

    path("account/", views.redirect_accounts, name = "accounts"),
    path("account/index/", include("accounts.urls")),

    path("class/", views.redirect_class_info, name = "class_info"),
    path("class/class_info/", include("class_info.urls")),

    path("seminar/", views.redirect_seminar_info, name = "seminar_info"),
    path("seminar/seminar_info/", include("seminar_info.urls")),

    path("circle/", views.redirect_circle_info, name = "circle_info"),
    path("circle/circle_info/", include("circle_info.urls")),

    path("shimmeringfuseda/", views.redirect_shimmeringfuseda, name = "shimmeingfuseda"),
    path("shimmeringfuseda/dubious/", include("shimmeringfuseda.urls"))
]