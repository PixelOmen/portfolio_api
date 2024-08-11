from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from . import models, serializers


class EmailTestView(APIView):
    def post(self, request):
        if not request.data.get('email'):
            return Response({'details': 'Email not provided'}, status=400)
        send_mail(
            'Django Mail',
            'This is a test email from Django.',
            settings.EMAIL_HOST_USER,
            [request.data['email']],
            fail_silently=False,
        )
        return Response({'details': request.data})


class ServerLimitsView(APIView):
    def get(self, _):
        return Response({
            'max_image_size': settings.MAX_IMAGE_SIZE,
            'max_user_images': settings.MAX_USER_IMAGES,
            'max_post_length': settings.MAX_POST_LENGTH,
            'allowed_image_extensions': settings.ALLOWED_IMAGE_EXTENSIONS,
        })


class TokenTestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, _):
        return Response({'details': 'You are authenticated!'})


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

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied(
                "You do not have permission to delete this Image")
        instance.image.delete(save=False)
        instance.delete()
