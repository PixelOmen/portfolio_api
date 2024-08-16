from django.db import models
from django.conf import settings


class UserPost(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class UserImage(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.FileField(upload_to='images/', null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

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
