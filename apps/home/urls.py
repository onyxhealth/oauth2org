from django.conf.urls import url
from django.contrib import admin
from .views import  (authenticated_home, id_token_payload_json, fetch_cda,
                     do_fetch_patient_data)


admin.autodiscover()

urlpatterns = [
    
    url(r'^fetch-cda-from-hie$', fetch_cda, name='fetch_cda'),
    url(r'^do-fetch-patient-data$', do_fetch_patient_data,
        name='do_fetch_patient_data'),
    # url(r'^do-patient-search$', do_patient_search, name='do_patient_search'),
    # url(r'^do-patient-activate$', do_patient_activate, name='do_patient_activate'),
    # url(r'^do-patient-consent-directive$', do_patient_consent_directive,
    #    name=do_patient_consent_directive),
    url(r'^id-token-payload$', id_token_payload_json, name='id_token_payload_json'),
    url(r'^', authenticated_home, name='home'),
]
