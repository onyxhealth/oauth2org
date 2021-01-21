from .mongoutils import query_mongo
from collections import OrderedDict
import uuid
from django.http import HttpResponse, Http404
import json
from django.conf import settings

# Copyright Videntity Systems, Inc. 2020


def format_search_result(entry):
    stub = OrderedDict()
    stub["resourceType"] = "Bundle"
    stub["id"] = str(uuid.uuid4())
    stub["type"] = "searchset"
    stub["total"] = len(entry)
    stub["entry"] = entry
    return stub


def fhir_read(request, fhir_resource_type, id):
    # Provider Directory public read.
    if fhir_resource_type not in ('Organization',
                                  'OrganizationAffiliation',
                                  'Practitioner',
                                  'PractitionerRole',
                                  'Endpoint',
                                  'Location',
                                  'HealthcareService',
                                  'InsurancePlan'):
        raise Http404

    q = query_mongo(database_name=settings.PROVIDER_DIRECTORY_MONGODB_DATABASE_NAME,
                    collection_name=fhir_resource_type,
                    query={'id': id})
    if q['results']:
        return HttpResponse(json.dumps(q['results'][0], indent=4),
                            content_type="application/json")
    else:
        raise Http404


def practitioner_fhir_search(request):

    query = dict(request.GET.items())

    if 'address-postalcode' in query.keys():
        query['address.postalCode'] = query['address-postalcode']
        del query['address-postalcode']

    if 'address-state' in query.keys():
        query['address.state'] = query['address-state'].upper()
        del query['address-state']

    if 'address-city' in query.keys():
        query['address.city'] = query['address-city'].upper()
        del query['address-city']

    if 'family' in query.keys():
        query['name.family'] = query['family'].upper()
        del query['family']

    if 'given' in query.keys():
        query['name.given'] = query['given'].upper()
        del query['given']

    if 'identifier' in query.keys():
        query['identifier.value'] = query['identifier']
        del query['identifier']

    if 'specialty' in query.keys():
        query['specialty.coding.code'] = query['specialty']
        del query['specialty']

    if 'communication-coding-code' in query.keys():
        query['communication.coding.code'] = query['communication-coding-code']
        del query['communication-coding-code']

    if 'location' in query.keys():
        query['location.reference'] = "Location/%s" % (query['location'])
        del query['location']

    if '_id' in query.keys():
        query['id'] = query['_id']
        del query['_id']

    q = query_mongo(database_name=settings.PROVIDER_DIRECTORY_MONGODB_DATABASE_NAME,
                    collection_name="Practitioner",
                    limit=settings.PROVIDER_DIRECTORY_SEARCH_LIMIT,
                    query=query
                    )
    response = format_search_result(q['results'])
    return HttpResponse(json.dumps(response, indent=4),
                        content_type="application/json")


def practitionerrole_fhir_search(request):

    query = dict(request.GET.items())

    if 'organization' in query.keys():
        query['organization.reference'] = "Organization/%s" % (query['organization'])
        del query['organization']

    if 'practitioner' in query.keys():
        query['organization.reference'] = "Practitioner/%s" % (query['practitioner'])
        del query['practitioner']

    if 'location' in query.keys():
        query['location.reference'] = "Location/%s" % (query['location'])
        del query['location']

    if 'specialty' in query.keys():
        query['specialty.coding.code'] = query['specialty']
        del query['specialty']

    if 'identifier' in query.keys():
        query['identifier.value'] = query['identifier']
        del query['identifier']

    if 'communication-coding-code' in query.keys():
        query['communication.coding.code'] = query['communication-coding-code']
        del query['communication-coding-code']

    if '_id' in query.keys():
        query['id'] = query['_id']
        del query['_id']

    q = query_mongo(database_name=settings.PROVIDER_DIRECTORY_MONGODB_DATABASE_NAME,
                    collection_name="PractitionerRole",
                    limit=settings.PROVIDER_DIRECTORY_SEARCH_LIMIT,
                    query=query
                    )
    response = format_search_result(q['results'])
    return HttpResponse(json.dumps(response, indent=4),
                        content_type="application/json")


def organization_fhir_search(request):
    query = dict(request.GET.items())
    if 'identifier' in query.keys():
        query['identifier.coding.value'] = query['identifier']
        del query['identifier']
    if '_id' in query.keys():
        query['id'] = query['_id']
        del query['_id']

    if 'name' in query.keys():
        query['name'] = query['name'].upper()
        del query['name']
    if 'location' in query.keys():
        query['location.reference'] = "Location/%s" % (query['location'])
        del query['location']

    if 'address-postalcode' in query.keys():
        query['address.postalCode'] = query['address-postalcode']
        del query['address-postalcode']

    if 'address-state' in query.keys():
        query['address.state'] = query['address-state'].upper()
        del query['address-state']

    q = query_mongo(database_name=settings.PROVIDER_DIRECTORY_MONGODB_DATABASE_NAME,
                    collection_name="Organization",
                    limit=settings.PROVIDER_DIRECTORY_SEARCH_LIMIT,
                    query=query
                    )
    response = format_search_result(q['results'])
    return HttpResponse(json.dumps(response, indent=4),
                        content_type="application/json")


def organizationaffiliation_fhir_search(request):
    query = dict(request.GET.items())
    if 'identifier' in query.keys():
        query['identifier.coding.value'] = query['identifier']
        del query['identifier']
    if '_id' in query.keys():
        query['id'] = query['_id']
        del query['_id']

    if 'name' in query.keys():
        query['name'] = query['name'].upper()
        del query['name']

    if 'location' in query.keys():
        query['location.reference'] = "Location/%s" % (query['location'])
        del query['location']

    q = query_mongo(database_name=settings.PROVIDER_DIRECTORY_MONGODB_DATABASE_NAME,
                    collection_name="OrganizationAffiliation",
                    limit=settings.PROVIDER_DIRECTORY_SEARCH_LIMIT,
                    query=query
                    )
    response = format_search_result(q['results'])
    return HttpResponse(json.dumps(response, indent=4),
                        content_type="application/json")


def endpoint_fhir_search(request):
    query = dict(request.GET.items())
    if 'identifier' in query.keys():
        query['identifier.coding.value'] = query['identifier']
        del query['identifier']
    if '_id' in query.keys():
        query['id'] = query['_id']
        del query['_id']
    if 'name' in query.keys():
        query['name'] = query['name'].upper()
        del query['name']
    if 'organization' in query.keys():
        query['organization.reference'] = "Organization/%s" % (query['organization'])
        del query['organization']

    q = query_mongo(database_name=settings.PROVIDER_DIRECTORY_MONGODB_DATABASE_NAME,
                    collection_name="Endpoint",
                    limit=settings.PROVIDER_DIRECTORY_SEARCH_LIMIT,
                    query=query
                    )
    response = format_search_result(q['results'])
    return HttpResponse(json.dumps(response, indent=4),
                        content_type="application/json")


def healthcareservice_fhir_search(request):
    query = dict(request.GET.items())
    if 'identifier' in query.keys():
        query['identifier.coding.value'] = query['identifier']
        del query['identifier']
    if '_id' in query.keys():
        query['id'] = query['_id']
        del query['_id']
    if 'address-postalcode' in query.keys():
        query['address.postalCode'] = query['address-postalcode']
        del query['address-postalcode']

    if 'address-state' in query.keys():
        query['address.state'] = query['address-state'].upper()
        del query['address-state']

    if 'address-city' in query.keys():
        query['address.city'] = query['address-city'].upper()
        del query['address-city']
    q = query_mongo(database_name=settings.PROVIDER_DIRECTORY_MONGODB_DATABASE_NAME,
                    collection_name="HealthcareService",
                    limit=settings.PROVIDER_DIRECTORY_SEARCH_LIMIT,
                    query=query
                    )
    response = format_search_result(q['results'])
    return HttpResponse(json.dumps(response, indent=4),
                        content_type="application/json")


def insuranceplan_fhir_search(request):
    query = dict(request.GET.items())
    if 'identifier' in query.keys():
        query['identifier.coding.value'] = query['identifier']
        del query['identifier']
    if '_id' in query.keys():
        query['id'] = query['_id']
        del query['_id']
    if 'address-postalcode' in query.keys():
        query['address.postalCode'] = query['address-postalcode']
        del query['address-postalcode']

    if 'address-state' in query.keys():
        query['address.state'] = query['address-state'].upper()
        del query['address-state']

    if 'address-city' in query.keys():
        query['address.city'] = query['address-city'].upper()
        del query['address-city']

    q = query_mongo(database_name=settings.PROVIDER_DIRECTORY_MONGODB_DATABASE_NAME,
                    collection_name="InsurancePlan",
                    limit=settings.PROVIDER_DIRECTORY_SEARCH_LIMIT,
                    query=query
                    )
    response = format_search_result(q['results'])
    return HttpResponse(json.dumps(response, indent=4),
                        content_type="application/json")


def location_fhir_search(request):
    query = dict(request.GET.items())
    if 'identifier' in query.keys():
        query['identifier.coding.value'] = query['identifier']
        del query['identifier']
    if '_id' in query.keys():
        query['id'] = query['_id']
        del query['_id']

    if 'address-postalcode' in query.keys():
        query['address.postalCode'] = query['address-postalcode']
        del query['address-postalcode']

    if 'address-state' in query.keys():
        query['address.state'] = query['address-state'].upper()
        del query['address-state']

    if 'address-city' in query.keys():
        query['address.city'] = query['address-city'].upper()
        del query['address-city']

    q = query_mongo(database_name=settings.PROVIDER_DIRECTORY_MONGODB_DATABASE_NAME,
                    collection_name="Location",
                    limit=settings.PROVIDER_DIRECTORY_SEARCH_LIMIT,
                    query=query
                    )
    response = format_search_result(q['results'])
    return HttpResponse(json.dumps(response, indent=4),
                        content_type="application/json")
