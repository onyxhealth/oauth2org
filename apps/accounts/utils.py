from jwkest.jwt import JWT


def get_id_token_payload(user):
    # Get the ID Token and parse it, return a JSON string.
    try:
        provider = user.social_auth.filter(
            provider='verifymyidentity-openidconnect').first()
        if 'id_token' in provider.extra_data.keys():
            id_token = provider.extra_data.get('id_token')
            parsed_id_token = JWT().unpack(id_token).payload()
        else:
            parsed_id_token = {'sub': '', 'ial': '1'}

    except Exception:
        parsed_id_token = {'sub': '', 'ial': '1'}

    return parsed_id_token
