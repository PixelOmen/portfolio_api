from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from . import debug

api_v1_router = DefaultRouter()
api_v1_router.register(
    r'user-posts', views.UserPostViewSet, basename='user-posts')
api_v1_router.register(
    r'user-images', views.UserImageViewSet, basename='user-images')

urlpatterns = [
    path('token-test/', views.TokenTestView.as_view(), name='token-test'),
    path('server-limits/', views.ServerLimitsView.as_view(),
         name='server-limits'),
    path('user-messages/', views.UserMessageViewSet.as_view(),
         name='user-messages'),
    path('', include(api_v1_router.urls)),

    # --- Debug endpoints ---
    # path('email', debug.display_email_template, name='email'),
    # path('email-test/', debug.EmailTestView.as_view(), name='email-test'),
    # path('celery-test/', debug.CeleryTestView.as_view(), name='celery-test'),
]
