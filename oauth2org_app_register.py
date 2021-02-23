#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python 3.5+

import argparse
import json
from collections import OrderedDict
import requests
import base64
import uuid

__author__ = "Alan Viars"


def oauth2org_app_register(client_name, tenant, basic_http_auth_username, basic_http_auth_password,
                           application_type="web",
                           redirect_uris=[],
                           post_logout_redirect_uris=[],
                           grant_types=["authorization_code", "refresh_token", "implicit"],
                           response_types=["code", ],
                           initiate_login_uri=None,
                           logo_uri=None, client_uri=None,
                           token_endpoint_auth_method="client_secret_post",
                           client_id=None,
                           client_secret=None):
    response = OrderedDict()
    wellknown = requests.get("%s/.well-known/oauth-authorization-server" % (tenant))
    if wellknown.status_code == 200:
        wellknown = requests.get("%s/.well-known/openid-configuration" % (tenant))
        if wellknown.status_code == 200:
            wellknown_dict = json.loads(wellknown.text, object_pairs_hook=OrderedDict)
            url = wellknown_dict['registration_endpoint']
    else:
        response['error'] = "Could not get the wellknown endpoint." + \
            "Perhaps you are disconnected form the internet or suplied the wrong URL."
        return response

    if not initiate_login_uri:
        initiate_login_uri = "%s/social-auth/login/verifymyidentity-openidconnect/" % (tenant)
    request_body = OrderedDict()
    request_body['application_type'] = application_type
    request_body['client_name'] = client_name
    request_body['redirect_uris'] = redirect_uris
    if client_uri:
        request_body['client_uri'] = client_uri
    if client_id:
        request_body['client_id'] = client_id
    if client_secret:
        request_body['client_secret'] = client_secret
    if client_uri:
        request_body['client_uri'] = client_uri
    if logo_uri:
        request_body['logo_uri'] = logo_uri
    if post_logout_redirect_uris:
        request_body['post_logout_redirect_uris'] = post_logout_redirect_uris
    request_body['response_types'] = response_types
    request_body['grant_types'] = grant_types
    request_body['token_endpoint_auth_method'] = token_endpoint_auth_method
    request_body['initiate_login_uri'] = initiate_login_uri
    request_body['token_endpoint_auth_method'] = token_endpoint_auth_method
    # print(json.dumps(request_body, indent=4))
    user_and_pass = "%s:%s" % (basic_http_auth_username, basic_http_auth_password)
    encoded = base64.b64encode(user_and_pass.encode()).decode("ascii")
    auth_header_value = "Basic %s" % (encoded)
    headers = {"Content-Type": "application/json", "Authorization": auth_header_value}
    r = requests.post(url, json=request_body, headers=headers)
    if r.text:
        # print(r.text)
        response = json.loads(r.text, object_pairs_hook=OrderedDict)
    if r.status_code not in (200, 201):
        response["status_code"] = r.status_code
    return response


if __name__ == "__main__":
    # Parse args
    desc = """Input OAuth2org instance details and register an app into an OAuth2org"""
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument(dest='client_name', action='store',
                        help='The OAuth2org app label. Use quotes if whitespaces.')

    parser.add_argument(dest='tenant', action='store',
                        help='The OAuth2org tenant ID/hostname URL.')
    parser.add_argument(dest='basic_http_auth_username', action='store', help="Username for Basic HTTP Auth")
    parser.add_argument(dest='basic_http_auth_password', action='store', help="passowrd for Basic HTTP Auth")

    parser.add_argument('-a', '--application_type', dest='application_type', action='store', default="web",
                        help='The OAuth2org token_endpoint_application_type can be web, native, browser, service. web by default.')

    parser.add_argument('-u', '--client_uri', dest='client_uri', action='store',
                        help="The app's client_uri", default=None)

    parser.add_argument('-l', '--logo_uri', dest='logo_uri', action='store',
                        help='The apps logo uri', default=None)

    parser.add_argument('-i', '--initiate_login_uri', dest='initiate_login_uri', action='store',
                        help='The initiate_login_uri', default=None)

    parser.add_argument('-m', '--token_endpoint_auth_method', dest='token_endpoint_auth_method', action='store',
                        help='The OAuth2org token_endpoint_auth_method. Default is "client_secret_post"', default="client_secret_post")

    parser.add_argument('-c', '--redirect_uris', '--callbacks', dest='redirect_uris',
                        default=["https://www.example-application.com/oauth2/redirectUri", ],
                        nargs='+', action='store', help='One or more redirect_uris for the app being registered.')

    parser.add_argument('-s', '--client_secret', dest='client_secret', action='store',
                        help='The client_secret supplied by you', default=None)

    parser.add_argument('-d', '--client_id', dest='client_id', action='store',
                        help='The client_id supplied by you', default=str(uuid.uuid4()))
    parser.add_argument('-g', '--grant_types', dest='grant_types',
                        default=["authorization_code",
                                 "refresh_token", "implicit"],
                        nargs='+', action='store',
                        help='One or more grant_types for the app being registered. Default is ["authorization_code","refresh_token","implicit"]')

    parser.add_argument('-o', '--post_logout_redirect_uris', dest='post_logout_redirect_uris',
                        default=[],
                        nargs='+', action='store',
                        help='One or more post_logout_redirect_uris for the app being registered. Default is [], an empty list')

    parser.add_argument('-r', '--response_types', dest='response_types',
                        default=["code", ],
                        nargs='+', action='store',
                        help='One or more response_types for the app being registered. Default is ["code", "id_token"].')

    args = parser.parse_args()

    result = oauth2org_app_register(args.client_name,  args.tenant,
                                    args.basic_http_auth_username,
                                    args.basic_http_auth_password,
                                    args.application_type,
                                    args.redirect_uris,
                                    args.post_logout_redirect_uris,
                                    args.grant_types,
                                    args.response_types,
                                    args.initiate_login_uri,
                                    args.logo_uri,
                                    args.client_uri,
                                    args.token_endpoint_auth_method,
                                    args.client_id,
                                    args.client_secret,
                                    )
    # output the OAuuth2org HTTP POST Response
    print(json.dumps(result, indent=4))
