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
