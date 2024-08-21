from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def ecs_health_check(request):
    return HttpResponse("OK", status=200)


urlpatterns = [
    path("health/", ecs_health_check),
    path("backdoor/", admin.site.urls),
    path("api/v1/", include("api.urls")),
    path("socialauth/", include("socialauth.urls")),
]
