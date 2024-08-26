from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, MethodNotAllowed

from . import models, serializers, tasks
from .throttling import (
    AnonDailyThrottle,
    AnonBurstRateThrottle,
    UserDailyImageThrottle,
    UserBurstImageThrottle,
    UserBurstPostThrottle,
)


# ------------ Utility endpoints ------------
class UserLimitsView(APIView):
    """Server limits for the Frontend, not enforced by the API"""

    def get(self, _):
        user_limits = models.UserLimits.objects.get(name="default")
        serializer = serializers.UserLimitsSerializer(user_limits)
        return Response(serializer.data)


class TokenTestView(APIView):
    """
    Endpoint to simply test if the user is authenticated and
    send an email when they first associate their account.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.email and not request.user.welcome_email_sent:
            # Waiting for SES to be approved
            # tasks.send_welcome_email_task.delay(
            #     request.user.first_name, request.user.email
            # )  # type: ignore
            request.user.welcome_email_sent = True
            request.user.save()
        return Response({"details": "You are authenticated!"})


# ----------- Anon User Endpoints ------------
class AnonMessageViewSet(APIView):
    throttle_classes = [
        AnonDailyThrottle,
        AnonBurstRateThrottle,
        UserBurstPostThrottle,
    ]

    def post(self, request):
        serializer = serializers.AnonMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# ----------- Auth User Endpoints ------------
# Note: PermissionDenied exceptions are not really needed,
# querysets are filtered by owner, but why not?
class UserPostViewSet(ModelViewSet):
    serializer_class = serializers.UserPostSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserBurstPostThrottle]

    def get_queryset(self):
        return models.UserPost.objects.filter(owner=self.request.user)

    def get_throttles(self):
        if self.request.method == "POST":
            return super().get_throttles()
        return []

    def get_object(self):
        obj = super().get_object()
        if obj.owner != self.request.user:
            raise PermissionDenied("You do not have permission to access this Post")
        return obj

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this Post")
        serializer.save(owner=self.request.user)
        serializer.save(date_modified=timezone.now())

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to delete this Post")
        instance.delete()


class UserImageViewSet(ModelViewSet):
    serializer_class = serializers.UserImageSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserDailyImageThrottle, UserBurstImageThrottle]

    def get_throttles(self):
        if self.request.method == "POST":
            return super().get_throttles()
        return []

    def get_queryset(self):
        return models.UserImage.objects.filter(owner=self.request.user)

    def get_object(self):
        obj = super().get_object()
        if obj.owner != self.request.user:
            raise PermissionDenied("You do not have permission to access this Image")
        return obj

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, _):
        raise MethodNotAllowed("Update method not allowed on user images")

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to delete this Image")
        instance.image.delete(save=False)
        instance.delete()
