import json
from oauth2_provider.oauth2_backends import OAuthLibCore
from oauth2_provider.models import AccessToken
from .loggers import (clear_session_auth_flow_trace, update_session_auth_flow_trace_from_code,
                      set_session_auth_flow_trace_value)
from ..accounts.models import UserProfile


class OAuthLibSMARTonFHIR(OAuthLibCore):

    def create_token_response(self, request):
        """
        Add items to the access_token response to comply with
        SMART on FHIR Authorization
        http://docs.smarthealthit.org/authorization/
        """
        # Get session values previously stored in AuthFlowUuid from AuthorizationView.form_valid() from code.
        body = dict(self.extract_body(request))
        clear_session_auth_flow_trace(request)
        update_session_auth_flow_trace_from_code(request, body.get('code', None))
        set_session_auth_flow_trace_value(request, 'auth_grant_type', body.get('grant_type', None))

        uri, headers, body, status = super(OAuthLibSMARTonFHIR, self).create_token_response(request)

        if status == 200:
            fhir_body = json.loads(body)
            token = AccessToken.objects.get(token=fhir_body.get("access_token"))
            fhir_body["aud"] = token.application.client_id
            if UserProfile.objects.filter(user=token.user).exists():
                up = UserProfile.objects.get(user=token.user)
                fhir_body["patient"] = up.fhir_patient_id
                body = json.dumps(fhir_body)
        return uri, headers, body, status
