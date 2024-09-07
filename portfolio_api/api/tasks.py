import logging

from django.conf import settings
from celery import shared_task

from . import email


LOGGER = logging.getLogger("celery")


@shared_task()
def send_welcome_email_task(username: str, user_email: str):
    LOGGER.info(f"Sending Welcome Email to {user_email}")
    email.send_welcome_email(username, user_email)
    return f"Welcome Email sent"


@shared_task()
def send_anon_message_email_task(
    name: str, user_email: str, content: str, date_posted: str
):
    LOGGER.info("Sending Anon Message Email")
    subject = f"You got a Portfolio message from: {name}"
    message = f"Name: {name}\n\nEmail: {user_email}\n\nMessage:\n{content}\n\nDate: {date_posted}"
    recipient_list = [settings.EMAIL_HOST_USER]
    email.ea_send_mail(subject=subject, message=message, recipient_list=recipient_list)
    return f"Anon Message Email sent"
