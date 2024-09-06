import logging

from django.apps import apps
from celery import shared_task

from . import email, models
from wschat.models import UserChat


LOGGER = logging.getLogger("celery")


@shared_task()
def send_welcome_email_task(username: str, user_email: str):
    LOGGER.info(f"Sending Welcome Email to {user_email}")
    email.send_welcome_email(username, user_email)
    return f"Welcome Email sent"
