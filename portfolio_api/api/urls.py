from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

api_v1_router = DefaultRouter()
api_v1_router.register(
    r'user-posts', views.UserPostViewSet, basename='user-posts')
api_v1_router.register(
    r'user-images', views.UserImageViewSet, basename='user-images')

urlpatterns = [
    path('email-test/', views.EmailTestView.as_view(), name='email-test'),
    path('server-limits/', views.ServerLimitsView.as_view(),
         name='server-limits'),
    path('token-test/', views.TokenTestView.as_view(), name='token-test'),
    path('', include(api_v1_router.urls)),
]
