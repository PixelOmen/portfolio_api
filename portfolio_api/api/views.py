import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from . import models, serializers


class TokenTestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'details': 'You are authenticated!'})


class UserPostViewSet(ModelViewSet):
    queryset = models.UserPost.objects.all()
    serializer_class = serializers.UserPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def get_object(self):
        obj = super().get_object()
        if obj.owner != self.request.user:
            raise PermissionDenied(
                "You do not have permission to access this Post")
        return obj

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        serializer.save(date_posted=datetime.datetime.now())

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied(
                "You do not have permission to delete this Post")
        instance.delete()
