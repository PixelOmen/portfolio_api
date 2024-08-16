from django.conf import settings
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, MethodNotAllowed

from .throttling import AnonMessageThrottle
from . import models, serializers, email, tasks


# ------------ Utility endpoints ------------
class ServerLimitsView(APIView):
    """ Server limits for the Frontend, not enforced by the API """

    def get(self, _):
        return Response({
            'max_image_size': settings.MAX_IMAGE_SIZE,
            'max_user_images': settings.MAX_USER_IMAGES,
            'max_post_length': settings.MAX_POST_LENGTH,
            'allowed_image_extensions': settings.ALLOWED_IMAGE_EXTENSIONS,
        })


class TokenTestView(APIView):
    """
    Endpoint to simply test if the user is authenticated and
    send an email when they first associate their account.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.email and not request.user.welcome_email_sent:
            tasks.send_welcome_email_task.delay(
                request.user.first_name, request.user.email)  # type: ignore
            request.user.welcome_email_sent = True
            request.user.save()
        return Response({'details': 'You are authenticated!'})


# ----------- Anon User Endpoints ------------
class UserMessageViewSet(APIView):
    throttle_classes = [AnonMessageThrottle]

    def post(self, request):
        serializer = serializers.UserMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# ----------- Auth User Endpoints ------------

# Note: PermissionDenied exceptions are not needed because
# querysets are filtered by owner but it is an extra layer of security.


class UserPostViewSet(ModelViewSet):
    serializer_class = serializers.UserPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.UserPost.objects.filter(owner=self.request.user)

    def get_object(self):
        obj = super().get_object()
        if obj.owner != self.request.user:
            raise PermissionDenied(
                "You do not have permission to access this Post")
        return obj

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.owner != self.request.user:
            raise PermissionDenied(
                "You do not have permission to edit this Post")
        serializer.save(owner=self.request.user)
        serializer.save(date_modified=timezone.now())

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied(
                "You do not have permission to delete this Post")
        instance.delete()


class UserImageViewSet(ModelViewSet):
    serializer_class = serializers.UserImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.UserImage.objects.filter(owner=self.request.user)

    def get_object(self):
        obj = super().get_object()
        if obj.owner != self.request.user:
            raise PermissionDenied(
                "You do not have permission to access this Image")
        return obj

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, _):
        raise MethodNotAllowed("Update method not allowed on user images")

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied(
                "You do not have permission to delete this Image")
        instance.image.delete(save=False)
        instance.delete()
