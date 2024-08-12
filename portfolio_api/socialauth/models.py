from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    welcome_email_sent = models.BooleanField(default=False)
