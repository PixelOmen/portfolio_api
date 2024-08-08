from rest_framework import serializers

from . import models


class UserPostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    date_posted = serializers.DateTimeField(read_only=True)
    date_modified = serializers.DateTimeField(read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.UserPost
        fields = ['id', 'content', 'date_posted', 'date_modified', 'owner']
