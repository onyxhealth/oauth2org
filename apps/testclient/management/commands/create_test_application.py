
from django.core.management.base import BaseCommand
from oauth2_provider.models import Application
from oauth2_provider.models import AccessToken
from django.utils import timezone
from datetime import timedelta
from django.conf import settings


def create_application():
    Application.objects.filter(name="TestApp").delete()
    redirect_uri = "%s/testclient/callback" % (settings.HOSTNAME_URL)
    if not(redirect_uri.startswith("http://") or redirect_uri.startswith("https://")):
        redirect_uri = "https://" + redirect_uri
    a = Application.objects.create(name="TestApp",
                                   client_id="Testapp-client-id",
                                   client_secret="testapp-client-secret-foo-bar",
                                   redirect_uris=redirect_uri,
                                   client_type="confidential",
                                   authorization_grant_type="authorization-code")
    return a


def create_test_token(user, application):
    now = timezone.now()
    expires = now + timedelta(days=1)
    t = AccessToken.objects.create(user=user, application=application,
                                   token="sample-token-string",
                                   expires=expires)
    return t


class Command(BaseCommand):
    help = 'Create a test user and application for the test client'

    def handle(self, *args, **options):
        a = create_application()
        print("client_id:", a.client_id)
        print("client_secret:", a.client_secret)
        print("redirect_uri:", a.redirect_uris)
