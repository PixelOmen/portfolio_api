"""
Email module is only located here because they are just
utility functions that don't require an entire app.
"""

from django.conf import settings

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def ea_send_mail(subject: str, message: str,
                 recipient_list: list[str], fail_silently=False) -> int:
    """
    Basically send_mail but injects the email host user
    so I don't have to provide it every time.
    """
    return send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        fail_silently=fail_silently,
    )


def send_template_email(
    subject: str,
    message: str,  # plain text message if the recipient can't render HTML
    recipient_list: list[str],
    email_template: str = 'email_template.html',
    context: dict | None = None,
    fail_silently: bool = False
) -> int:
    """
    Send an email with an HTML template.
    """
    if context is None:
        context = {}

    html_content = render_to_string(email_template, context)

    msg = EmailMultiAlternatives(
        subject, message, settings.EMAIL_HOST_USER, recipient_list)
    msg.attach_alternative(html_content, "text/html")

    return msg.send(fail_silently=fail_silently)
