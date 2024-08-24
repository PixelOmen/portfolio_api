from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seed the database with default superuser."

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = settings.DEFAULT_SUPERUSER_USERNAME
        email = settings.DEFAULT_SUPERUSER_EMAIL
        password = settings.DEFAULT_SUPERUSER_PASSWORD
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                username=username, email=email, password=password
            )
            self.stdout.write(
                self.style.SUCCESS("Successfully created default superuser.")
            )
        else:
            self.stdout.write(self.style.SUCCESS("Default superuser already exists."))
