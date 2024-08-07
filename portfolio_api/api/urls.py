from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

api_v1_router = DefaultRouter()
api_v1_router.register(
    r'user-posts', views.UserPostViewSet)

urlpatterns = [
    path('v1/token-test/', views.TokenTestView.as_view(), name='token-test'),
    path('v1/', include(api_v1_router.urls)),
]
