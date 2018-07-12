from django.urls import include, path
from front_end.intro import views as intro_views

urlpatterns = [
    path('peculab/', intro_views.intro_peculab),
    path('mimir/', intro_views.intro_mimir),
    path('mimir/me/', include('front_end.me.urls')),
    path('mostfintech_demo/', include('front_end.demo.urls')),
]
