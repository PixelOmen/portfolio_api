from rest_framework import serializers

from . import models


class AllowedImageMimeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AllowedImageMimeType
        fields = ["name"]
        read_only_fields = ["id"]


class UserLimitsSerializer(serializers.ModelSerializer):
    allowed_image_mimes = serializers.SlugRelatedField(
        many=True,
        queryset=models.AllowedImageMimeType.objects.all(),
        slug_field="name",
    )

    class Meta:
        model = models.UserLimits
        fields = [
            "max_image_size",
            "max_user_images",
            "max_post_length",
            "allowed_image_mimes",
        ]
        read_only_fields = ["id"]


class UserPostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    date_posted = serializers.DateTimeField(read_only=True)
    date_modified = serializers.DateTimeField(read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.UserPost
        fields = ["id", "content", "date_posted", "date_modified", "owner"]


class UserImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    date_posted = serializers.DateTimeField(read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.UserImage
        fields = ["id", "image", "date_posted", "owner"]


class AnonMessageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    date_posted = serializers.DateTimeField(read_only=True)

    class Meta:
        model = models.AnonMessage
        fields = ["id", "name", "email", "content", "date_posted"]
