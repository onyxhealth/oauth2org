import logging
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_GET
from collections import OrderedDict
from django.conf import settings
from django.urls import reverse
logger = logging.getLogger('hhs_server.%s' % __name__)


@require_GET
def oauth_authorization_server(request):
    """
    Views that returns openid_configuration.
    """
    data = OrderedDict()
    issuer = base_issuer(request)
    data = build_endpoint_info(data, issuer=issuer)
    return JsonResponse(data)


def openid_configuration(request):
    return HttpResponseRedirect(reverse('oauth_authorization_server'))


@require_GET
def smart_configuration(request):
    """
    Views that returns openid_configuration.
    """
    data = OrderedDict()
    issuer = base_issuer(request)
    data = build_endpoint_info_smart(data, issuer=issuer)
    return JsonResponse(data)


def base_issuer(request):
    """
    define the base url for issuer

    """
    issuer = getattr(settings, 'HOSTNAME_URL', 'http://localhost:8000')

    if "http://" in issuer.lower():
        pass
    elif "https://" in issuer.lower():
        pass
    else:
        logger.debug("HOSTNAME_URL [%s] "
                     "does not contain http or https prefix. "
                     "Issuer:%s" % (settings.HOSTNAME_URL, issuer))
        # no http/https prefix in HOST_NAME_URL so we add it
        if request.is_secure():
            http_mode = 'https://'
        else:
            http_mode = 'http://'

        # prefix hostname with http/https://
        issuer = http_mode + issuer

    return issuer


def build_endpoint_info(data=OrderedDict(), issuer=""):
    data["issuer"] = issuer
    data["authorization_endpoint"] = issuer + \
        reverse('oauth2_provider:authorize')
    data["token_endpoint"] = issuer + \
        reverse('oauth2_provider:token')
    data["userinfo_endpoint"] = issuer + \
        reverse('user_profile')
    data["revocation_endpoint"] = issuer + reverse("oauth2_provider:revoke-token")
    data["introspection_endpoint"] = issuer + reverse("oauth2_provider:introspect")
    data["registration_endpoint"] = issuer + reverse("registration_endpoint")
    data["ui_locales_supported"] = ["en-US", ]
    data["op_tos_uri"] = settings.TOS_URI
    data["grant_types_supported"] = []
    for i in settings.GRANT_TYPES:
        data["grant_types_supported"].append(i[0])
    data["grant_types_supported"].append("refresh_token")
    data["response_types_supported"] = ["code", "token"]

    # Not part of spec but provides
    # information on what to call users and orgs in the server's context.
    data['person_title'] = settings.CALL_MEMBER
    data['person_title_plural'] = settings.CALL_MEMBER_PLURAL
    data['organization_title'] = settings.CALL_ORGANIZATION
    data['organization_title_plural'] = settings.CALL_ORGANIZATION_PLURAL
    if settings.FHIR_BASE_URI:
        data["fhir_uri"] = settings.FHIR_BASE_URI
    if settings.OPERATIONAL_MODALITY:
        data["operational_modality"] = settings.OPERATIONAL_MODALITY

    return data


def build_endpoint_info_smart(data=OrderedDict(), issuer=""):
    data["authorization_endpoint"] = issuer + \
        reverse('oauth2_provider:authorize')
    data["token_endpoint"] = issuer + \
        reverse('oauth2_provider:token')
    data["revocation_endpoint"] = issuer + reverse("oauth2_provider:revoke-token")
    data["introspection_endpoint"] = issuer + reverse("oauth2_provider:introspect")
    data["registration_endpoint"] = issuer + reverse("registration_endpoint")
    data["response_types_supported"] = ["code", "token"]
    data['scopes_supported'] = ["openid", "profile", "fhirUser", "patient/*.read", "offline_access"]
    data['capabilities'] = ["launch-standalone", ]
    return data
