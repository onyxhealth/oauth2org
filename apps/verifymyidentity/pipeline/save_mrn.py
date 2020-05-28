#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from jwkest.jwt import JWT
from ...hie.models import HIEProfile
import logging

logger = logging.getLogger('smh_debug')

# Copyright Videntity Systems Inc.

__author__ = "Alan Viars"


def save_mrn(backend, user, response, *args, **kwargs):
    # make sure there is a UserProfile object for the given User
    profile, created = HIEProfile.objects.get_or_create(user=user)
    if backend.name == 'verifymyidentity-openidconnect':

        # Save the id_token 'sub' to the UserProfile.subject
        if 'id_token' in response.keys():
            id_token = response.get('id_token')
            id_token_payload = JWT().unpack(id_token).payload()
            print(id_token_payload)
            docs = id_token_payload.get('document')
            print(docs)
            if docs:
                for doc in docs:
                    if doc.get('issuer') == "HIXNY" and doc.get('type') == "MPI":
                        profile.mrn = doc.get('num')
                        profile.save()
                        logger.info('MPI issued by %s sourced for %s %s from %s' %
                                    (doc.get('issuer'), user.first_name, user.last_name, backend.name))
