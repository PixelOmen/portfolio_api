from django.core.management.base import BaseCommand
from oauth2_provider.models import Application
from django.conf import settings


class Command(BaseCommand):
    help = 'Ensure that the OAuth2 application is created with the correct client ID and secret.'

    def handle(self, *args, **kwargs):
        app_name = 'EAPortfolio Google OAuth2 App'
        client_id = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
        client_secret = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET

        app, created = Application.objects.get_or_create(
            client_id=client_id,
            defaults={
                'client_secret': client_secret,
                'name': app_name,
                'client_type': Application.CLIENT_PUBLIC,
                'authorization_grant_type': Application.GRANT_PASSWORD,
                'hash_client_secret': False,
                'skip_authorization': False,
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(
                f'Successfully created OAuth2 application: {app_name}'))
        else:
            app.name = app_name
            app.client_id = client_id
            app.client_secret = client_secret
            app.save()
            self.stdout.write(self.style.SUCCESS(
                f'Existing OAuth2 application found. Updated credentials.'))
