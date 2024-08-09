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
        return self.id


class UserImage(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='images/', null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.id
