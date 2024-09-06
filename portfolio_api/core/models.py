from django.db import models


class AllowedImageMimeType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class UserLimits(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="default", unique=True)
    max_image_size = models.IntegerField(default=0)
    max_user_images = models.IntegerField(default=0)
    max_post_length = models.IntegerField(default=0)
    max_chat_messages = models.IntegerField(default=0)
    allowed_image_mimes = models.ManyToManyField(
        AllowedImageMimeType, related_name="allowed_image_mimes"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "User Limits"
