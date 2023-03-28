from django.contrib import admin
from django.urls import path, include
from companies.urls import router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("companies.urls")),
]
