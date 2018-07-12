from django.urls import include, path

urlpatterns = [
    path('analyze/', include('api.analyze.urls')),
    path('preprocess/', include('api.preprocess.urls')),
    # path('account/', include('api.account.urls')),
]
