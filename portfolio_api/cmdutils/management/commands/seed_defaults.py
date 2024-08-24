from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seed the database with default UserLimits and default OAuth2 application."

    def handle(self, *args, **kwargs):
        call_command("seed_superuser")
        call_command("seed_userlimits")
        call_command("seed_oauth_app")
