from django.conf.urls import url
from .views import oauth_authorization_server, openid_configuration, smart_configuration


urlpatterns = [
    # openid-configuration -----------------------------------
    url(r'^oauth-authorization-server$',
        oauth_authorization_server,
        name='oauth_authorization_server'),
    url(r'^openid-configuration$',
        openid_configuration,
        name='openid-configuration'),
    url(r'^smart-configuration$',
        smart_configuration,
        name='smart-configuration'),
]
