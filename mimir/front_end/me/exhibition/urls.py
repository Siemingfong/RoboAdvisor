from django.urls import include, path
from .views import *

urlpatterns = [
    path('test/', test)
    # path('rawtext', rawtext),
    # path('corpus', corpus),
    # path('preprocessed', preprocessed),
    # path('result', result)
]
