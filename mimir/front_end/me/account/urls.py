from django.urls import path
from . import views as account_views

urlpatterns = [
    path('logout/', account_views.logout, name='logout'),
]
