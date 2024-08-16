import logging
from celery import shared_task

from . import email


@shared_task
def beat_task():
    logging.info("Beat Task")
    return "Beat Task Done"


@shared_task(bind=True)
def send_welcome_email_task(self, username: str, user_email: str):
    email.send_welcome_email(username, user_email)
    return f"Welcome Email sent"
