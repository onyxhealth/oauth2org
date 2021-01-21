import logging
# from django.conf import settings
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from jwkest.jwt import JWT
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
# Copyright Videntity Systems Inc.

__author__ = "Alan Viars"

logger = logging.getLogger('oauth2org_debug')


@login_required
def id_token_payload_json(request):

    try:
        vmi = request.user.social_auth.filter(
            provider='verifymyidentity-openidconnect')[0]
        extra_data = vmi.extra_data
        if 'id_token' in vmi.extra_data.keys():
            id_token = extra_data.get('id_token')
            parsed_id_token = JWT().unpack(id_token)
            parsed_id_token = parsed_id_token.payload()
    except Exception:
        id_token = "No ID token."
        parsed_id_token = {'sub': '', 'ial': '1',
                           "note": "No ID token for this user"}
    return JsonResponse(parsed_id_token)


def authenticated_home(request):
    name = _('Authenticated Home')
    if request.user.is_authenticated:
        # Get the ID Token and parse it.
        try:
            vmi = request.user.social_auth.filter(
                provider='verifymyidentity-openidconnect')[0]
            extra_data = vmi.extra_data
            if 'id_token' in vmi.extra_data.keys():
                id_token = extra_data.get('id_token')
                parsed_id_token = JWT().unpack(id_token)
                parsed_id_token = parsed_id_token.payload()

        except Exception:
            id_token = "No ID token."
            parsed_id_token = {'sub': '', 'ial': '1'}

        if parsed_id_token.get('ial') not in ('2', '3'):
            # redirect to get verified
            messages.warning(request, 'Your identity has not been verified. \
                             This must be completed prior to access to Personal Health Information.')
        try:
            profile = request.user.userprofile
        except Exception:
            profile = None

        # this is a GET
        context = {'name': name, 'profile': profile,
                   'id_token': id_token,
                   'id_token_payload': parsed_id_token}

        template = settings.HOMEPAGE_AUTHENTICATED_TEMPLATE
    else:
        name = ('home')
        context = {'name': name}
        template = settings.HOMEPAGE_TEMPLATE

    return render(request, template, context)
