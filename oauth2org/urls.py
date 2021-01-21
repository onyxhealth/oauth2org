"""oauth2org OAuth2 Provider  URL Configuration"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from apps.home.views import authenticated_home
from oauth2_provider import views
from apps.hie.decorators import check_ial_before_allowing_authorize
from django.conf import settings
# from django.views.generic import TemplateView
# from . import signals  # noqa
from .utils import IsAppInstalled

__author__ = "Alan Viars"

admin.site.site_header = "OAuth2org"
admin.site.site_title = "OAuth2/FHIR/SMART Server Admin Portal"
admin.site.index_title = "Oauth2org: OAuth2/FHIR/SMART Server Site Administration"

ADMIN_PATH = "%sadmin/" % (settings.ADMIN_REDIRECTOR)

urlpatterns = [
    path('admin/', admin.site.urls),
    url('social-auth/', include('social_django.urls', namespace='social')),
    path('accounts/', include('apps.accounts.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^home/', include('apps.home.urls')),
    url(r"^o/authorize/$",
        check_ial_before_allowing_authorize(views.AuthorizationView.as_view()), name="authorize"),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^.well-known/', include('apps.wellknown.urls')),
    path('dcrp/', include('apps.dynamicreg.urls')),
    # Sample API
    url(r'^api/', include('apps.api.urls')),

    # Test Client
    url(r'^testclient/', include('apps.testclient.urls')),

    # This is the native Provider directory support using MongoDB
    url(r'^provider-directory/', include('apps.provider_directory.urls')),

    # These is the native patient-facing FHIR support using MongoDB
    url(r'^patient-api/', include('apps.patientface_api.urls')),

    # For MS Azure FHIR Proxy. Diabled by default.
    # url(r'^fhir/', include('apps.fhirproxy.urls')), # Used for MS Azure
    # Backend.

    # The next HIE URLs are for InterSystems Support. Disabled by default.
    # url(r'^rhio/', include('apps.hie.urls')),
    # url(r'^hie/', include('apps.hie.urls')),
    # url(r'^hixny/', include('apps.hie.urls')),

    path('', authenticated_home, name='home'),


]

if IsAppInstalled("djmongo"):
    urlpatterns += [
        url(r'^djm/', include('djmongo.urls')),
    ]

if IsAppInstalled("apps.adt"):
    urlpatterns += [
        url(r'^adt/', include('apps.adt.urls')),
    ]
