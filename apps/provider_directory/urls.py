from django.conf.urls import include, url
from django.contrib import admin
from .views import (practitioner_fhir_search, organization_fhir_search,
                    practitioner_fhir_read, organization_fhir_read)

admin.autodiscover()

# Copyright Videntity Systems, Inc. 2020

fhir4 = [
     url(r'Practitioner/(?P<id>[^/]+)', practitioner_fhir_read, name="practitioner_fhir_read"),
     url(r'Organization/(?P<id>[^/]+)', organization_fhir_read, name="organization_fhir_read"),
     url(r'Practitioner', practitioner_fhir_search, name="practitioner_fhir_search"),
     url(r'Organization', organization_fhir_search, name="organization_fhir_search"),
    
]

urlpatterns = [
    url('fhir4/', include(fhir4)),
]
