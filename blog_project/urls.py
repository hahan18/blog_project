from django.contrib import admin
from django.urls import path
from .main_api import main_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', main_api.urls),
]
