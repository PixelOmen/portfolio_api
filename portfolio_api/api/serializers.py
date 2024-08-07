from rest_framework import serializers

from . import models


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserPost
        fields = '__all__'
