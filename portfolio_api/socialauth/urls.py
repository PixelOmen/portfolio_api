from django.urls import path, include, re_path

from . import views

urlpatterns = [
    path('google/', views.GoogleAuthToTokenView.as_view(), name='googleauth'),
    re_path(r'^drfso2/', include('drf_social_oauth2.urls', namespace='drf'))
]
