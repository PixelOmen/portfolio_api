import logging
from celery import shared_task
from django.conf import settings

from . import email, models


LOGGER = logging.getLogger("celery")


@shared_task
def user_data_reset_task():
    LOGGER.info("Resetting User Data")
    for img in models.UserImage.objects.all():
        img.image.delete(save=False)
        img.delete()
    models.UserPost.objects.all().delete()
    return "User Data Reset"


@shared_task()
def send_welcome_email_task(username: str, user_email: str):
    LOGGER.info(f"Sending Welcome Email to {user_email}")
    LOGGER.info(f"password: {settings.EMAIL_HOST_PASSWORD}")
    email.send_welcome_email(username, user_email)
    return f"Welcome Email sent"
