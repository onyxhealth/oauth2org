"""oauth2org OAuth2 Provider URL Configuration"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from apps.home.views import authenticated_home
from oauth2_provider import views
from apps.hie.decorators import check_ial_before_allowing_authorize
# from django.views.generic import TemplateView
# from . import signals  # noqa
from .utils import IsAppInstalled

# make the admin URL a shared secret in production by setting this.
# for exmple, if ADMIN_REDIRECTOR == "hello-", the admin URL will be /hello-admin/
ADMIN_REDIRECTOR = getattr(settings, 'ADMIN_PREPEND_URL', '')

__author__ = "Alan Viars"

admin.site.site_header = "OAuth2org"
admin.site.site_title = "OAuth2/FHIR/SMART Server Admin Portal"
admin.site.index_title = "Oauth2org: OAuth2/FHIR/SMART Server Site Administration"


ADMIN_PATH = "%sadmin/" % (settings.ADMIN_REDIRECTOR)


urlpatterns = [
    path(ADMIN_PATH, admin.site.urls),  # make the admin URL a shared secret in production.
    url('social-auth/', include('social_django.urls', namespace='social')),
    path('accounts/', include('apps.accounts.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^home/', include('apps.home.urls')),
    url(r"^o/authorize/$",
        check_ial_before_allowing_authorize(views.AuthorizationView.as_view()), name="authorize"),
    url(r'^fhir/', include('apps.fhir.bluebutton.urls')),
    url(r'o/', include('apps.dot_ext.urls')),
    # url(r'^/o/', include('apps.authorization.urls')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^.well-known/', include('apps.wellknown.urls')),
    path('dcrp/', include('apps.dynamicreg.urls')),

    # Test Client for Patient Facing App.
    url(r'^testclient/', include('apps.testclient.urls')),
    # For MS Azure FHIR Proxy. Diabled by default.
    # url(r'^fhir/', include('apps.fhirproxy.urls')), # Used for MS Azure
    # Backend.
    path('', authenticated_home, name='home'),
]

# MongoDB-based Patient API.
if IsAppInstalled("apps.provider_directory"):
    urlpatterns += [
        url(r'^provider-directory/', include('apps.provider_directory.urls')),
    ]


# MongoDB-based Patient API.
if IsAppInstalled("apps.patientface_api"):
    urlpatterns += [
        url(r'^patient-api/', include('apps.patientface_api.urls')),
    ]


# For apps managed in Microsoft Azure B2C.
if IsAppInstalled("apps.appman"):
    urlpatterns += [
        url(r'^appman/', include('apps.appman.urls')),
    ]

# For Microsoft Azure FHIR Proxy or HAPI SmileCDR Proxy configutations.
if IsAppInstalled("apps.apps.fhirproxy"):
    urlpatterns += [
        url(r'^fhir/', include('apps.fhirproxy.urls')),
    ]


if IsAppInstalled("apps.hie"):
    urlpatterns += [
        url(r'^hie/', include('apps.hie.urls')),
        url(r'^api/', include('apps.api.urls')),
    ]

if IsAppInstalled("djmongo"):
    urlpatterns += [
       # url(r'^djm/', include('djmongo.urls')),
    ]

if IsAppInstalled("apps.adt"):
    urlpatterns += [
        url(r'^adt/', include('apps.adt.urls')),
    ]
