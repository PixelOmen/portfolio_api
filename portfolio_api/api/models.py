from django.db import models
from django.conf import settings


class AllowedImageMimeType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class UserLimits(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="default", unique=True)
    max_image_size = models.IntegerField()
    max_user_images = models.IntegerField()
    max_post_length = models.IntegerField()
    allowed_image_mimes = models.ManyToManyField(
        AllowedImageMimeType, related_name="allowed_image_mimes"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "User Limits"


class UserPost(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class UserImage(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.FileField(upload_to="images/", null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class AnonMessage(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    content = models.TextField(null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f"{self.name}")
