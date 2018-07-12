from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('peculab/', peculab_home),
    path('mimir/', mimir_home)
]
