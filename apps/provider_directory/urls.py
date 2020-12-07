from django.conf.urls import include, url
from django.contrib import admin
from .views import (fhir_read,
                    practitioner_fhir_search,
                    practitionerrole_fhir_search,
                    organization_fhir_search,
                    organizationaffiliation_fhir_search,
                    location_fhir_search, endpoint_fhir_search,
                    insuranceplan_fhir_search, healthcareservice_fhir_search,
                    )

admin.autodiscover()

# Copyright Videntity Systems, Inc. 2020

fhir4 = [
    # Read
    url(r'(?P<fhir_resource_type>[^/]+)/(?P<id>[^/]+)', fhir_read, name="fhir_read"),

    # Search
    url(r'PractitionerRole', practitionerrole_fhir_search,
        name="practitionerrole_fhir_search"),
    url(r'Practitioner', practitioner_fhir_search, name="practitioner_fhir_search"),

    url(r'Organization', organization_fhir_search, name="organization_fhir_search"),
    url(r'OrganizationAffiliation', organizationaffiliation_fhir_search,
        name="organizationaffiliation_fhir_search"),
    url(r'Location', location_fhir_search, name="location_fhir_search"),
    url(r'Endpoint', endpoint_fhir_search, name="endpoint_fhir_search"),
    url(r'InsurancePlan', insuranceplan_fhir_search, name="insuranceplan_fhir_search"),
    url(r'HealthcareService', healthcareservice_fhir_search,
        name="healthcareservice_fhir_search"),
]

urlpatterns = [
    url('fhir4/', include(fhir4)),
]
