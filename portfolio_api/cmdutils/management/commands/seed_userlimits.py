from django.conf import settings
from django.core.management.base import BaseCommand

from core.models import UserLimits, AllowedImageMimeType


class Command(BaseCommand):
    help = (
        "Seed the database with default values for UserLimits and AllowedImageMimeType."
    )

    def handle(self, *args, **kwargs):
        mimes = settings.USER_LIMITS.get("DEFAULT_ALLOWED_IMAGE_MIMES")
        max_image_size = settings.USER_LIMITS.get("DEFAULT_MAX_IMAGE_SIZE")
        max_user_images = settings.USER_LIMITS.get("DEFAULT_MAX_USER_IMAGES")
        max_post_length = settings.USER_LIMITS.get("DEFAULT_MAX_POST_LENGTH")
        max_chat_messages = settings.USER_LIMITS.get("DEFAULT_MAX_CHAT_MESSAGES")

        for userlimit in [mimes, max_image_size, max_user_images, max_post_length]:
            if userlimit is None:
                raise ValueError(
                    "One or more of the default user limits are not set in settings.py."
                )

        default_limits, created_userlimits = UserLimits.objects.get_or_create(
            max_image_size=max_image_size,
            max_user_images=max_user_images,
            max_post_length=max_post_length,
            max_chat_messages=max_chat_messages,
        )
        if created_userlimits:
            self.stdout.write(
                self.style.SUCCESS("Successfully seeded default user limits.")
            )
        else:
            self.stdout.write(self.style.SUCCESS("Default user limits already exist."))

        created_mimes = False
        for mime in mimes:
            _, created = AllowedImageMimeType.objects.get_or_create(name=mime)
            if created:
                created_mimes = True
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully added default image mime type: {mime}"
                    )
                )

        if created_mimes:
            default_limits.allowed_image_mimes.set(AllowedImageMimeType.objects.all())
            self.stdout.write(
                self.style.SUCCESS("Successfully added all allowed image mime types.")
            )
        else:
            self.stdout.write(self.style.SUCCESS("No new image mime types were added."))
