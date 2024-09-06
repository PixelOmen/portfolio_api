import logging

from django.apps import apps
from celery import shared_task


LOGGER = logging.getLogger("celery")


@shared_task
def user_data_reset_task():
    LOGGER.info("Resetting User Data")
    UserImage = apps.get_model("api", "UserImage")
    UserPost = apps.get_model("api", "UserPost")
    UserChat = apps.get_model("wschat", "UserChat")
    for img in UserImage.objects.all():
        img.image.delete(save=False)  # type: ignore
        img.delete()
    UserPost.objects.all().delete()
    UserChat.objects.all().delete()
    return "User Data Reset"
