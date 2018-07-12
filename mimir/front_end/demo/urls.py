from django.urls import include, path
from .views import *

urlpatterns = [
    # path('coshow/', coshow),
    # path('btcprice/', btcprice),
    path('intro/', intro),
    path('history/', history),
    path('trafficlight/', traffic_light),
    path('textmining/', textmining),
    path('text_analyze/', text_analyze),
    # path('dm_fb_info_send/', dm_fb_info_send),
    # path('dm_fb_check_user_state/', dm_fb_check_user_state),
    # path('dm_user_account/', dm_user_account)
]
