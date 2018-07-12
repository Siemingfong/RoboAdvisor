from django.urls import include, path
from front_end.me import views as me_views 

urlpatterns = [
    path('exhibition/', include('front_end.me.exhibition.urls')),
    path('account/', include('front_end.me.account.urls')),
    path('', me_views.me),
]
