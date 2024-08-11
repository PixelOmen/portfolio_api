from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('backdoor/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('socialauth/', include('socialauth.urls')),
]
