"""
Email module is only located here because they are just
utility functions that don't require an entire app.
"""

from django.conf import settings

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def plain_text_message(user: str, contact_email: str, portfolio_link: str) -> str:
    return f"""Hi {user},\n\nThank you for visiting my site! I'm grateful that you've decided to explore the projects and demos I've put together. Your interest means a lot to me. If you'd like to work together, or just have any questions or feedback, please don't hesitate to reach out to me at {contact_email}.\n\nBest,\nEmmanuel Acosta\nPortfolio: {portfolio_link}\n\n\n\nThis is an automated message.\nYou will not receive any further emails.\nYou're receiving this email because you associated your google email with my app for the first time."""


def ea_send_mail(subject: str, message: str,
                 recipient_list: list[str], fail_silently=False) -> int:
    """
    Basically send_mail but injects the email host user.
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


def send_welcome_email(request, html: bool = True, fail_silently: bool = True) -> int:
    """ Send a welcome email to the user. """
    if html:
        return send_template_email(
            subject="Emmanuel's Portfolio - Welcome!",
            message=plain_text_message(
                request.user, settings.CONTACT_EMAIL, settings.EMAIL_PORTFOLIO_LINK),
            recipient_list=[request.user.email],
            context={'user': request.user,
                     'portfolio_link': settings.EMAIL_PORTFOLIO_LINK},
            fail_silently=fail_silently
        )
    else:
        return ea_send_mail(
            subject="Emmanuel's Portfolio - Welcome!",
            message=plain_text_message(
                request.user, settings.CONTACT_EMAIL, settings.EMAIL_PORTFOLIO_LINK),
            recipient_list=[request.user.email],
            fail_silently=fail_silently
        )
