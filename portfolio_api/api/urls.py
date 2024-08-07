from django.urls import path, include

from . import views

urlpatterns = [
    path('v1/token-test/', views.TokenTestView.as_view(), name='token-test'),
]
