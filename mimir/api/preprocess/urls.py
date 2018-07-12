from django.urls import path
from .views import *

urlpatterns = [
    path('test_tokenize_ch/', test_tokenize_ch)
]
