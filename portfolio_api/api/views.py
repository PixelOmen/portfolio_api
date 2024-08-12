from django.conf import settings
from django.utils import timezone

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, MethodNotAllowed

from . import models, serializers, email


#  ------------ Debug ------------
class EmailTestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        result = email.send_welcome_email(request, html=False)
        if result:
            return Response({'details': 'Email sent successfully'})
        else:
            return Response({'details': 'Email failed to send'}, status=500)


def display_email_template(request):
    context = {'user': request.user,
               'portfolio_link': settings.EMAIL_PORTFOLIO_LINK,
               'email_logo_url': settings.EMAIL_LOGO_URL}
    return render(request, 'email_template.html', context)


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
            email.send_welcome_email(request)
            request.user.welcome_email_sent = True
            request.user.save()
        return Response({'details': 'You are authenticated!'})


# ------------ User data ViewSets ------------

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
