from django.http import JsonResponse, Http404
from collections import OrderedDict
from django.shortcuts import get_object_or_404
from django.conf import settings
from datetime import datetime
from django.views.decorators.http import require_GET
from oauth2_provider.decorators import protected_resource
from .models import Crosswalk
from .mongo_utils import query_mongo
from bson import ObjectId
from .metadata import patient_facing_api_metadata_str
import json
from ..accounts.models import UserProfile

__author__ = "Alan Viars"


@require_GET
def fhir_metadata_endpoint(request):
    return JsonResponse(json.loads(patient_facing_api_metadata_str, object_pairs_hook=OrderedDict))


@require_GET
@protected_resource()
def fhir_endpoint_with_id(request, fhir_resource, id):
    tied_to_patient = False
    if fhir_resource not in settings.FHIR_PATIENT_API_RESOURCES_SUPPORTED:
        raise Http404

    up = UserProfile.objects.get(user=request.resource_owner)
    if up.fhir_patient_id != id and fhir_resource == "Patient":
        # Do not allow mismatched token/user/fhir ID
        raise Http404
    elif up.fhir_patient_id == id and fhir_resource == "Patient":
        tied_to_patient = True

    d = query_mongo(settings.PATIENT_ACCESS_MONGODB_DATABASE_NAME, fhir_resource, query={"id": id}, limit=1)

    if not d["results"]:
        raise Http404("No results found")
    one_result = d["results"][0]

    if "_id" in one_result.keys():
        del one_result['_id']

    if "id" in one_result.keys():
        if isinstance(one_result["id"], ObjectId):
            one_result["id"] = str(one_result["id"])

    # Return only a single FHIR Resource
    if 'subject' in one_result.keys():
        if 'reference' in one_result['subject'].keys():
            if one_result['subject']['reference'] == "Patient/%s" % (up.fhir_patient_id):
                tied_to_patient = True
    if 'patient' in one_result.keys():
        if 'reference' in one_result['patient'].keys():
            if one_result['patient']['reference'] == "Patient/%s" % (up.fhir_patient_id):
                tied_to_patient = True

    if tied_to_patient is False:
        raise Http404("This record is not tied to the patient.")
    return JsonResponse(one_result)


def make_bundle(docs):
    cleaned_entries = []
    for r in docs['results']:
        if '_id' in r.keys():
            del r['_id']
        cleaned_entries.append(r)
    od = OrderedDict()
    od["resourceType"] = "Bundle"
    od["type"] = "searchset"
    od["meta"] = {"lastUpdated": "%sZ" % (str(datetime.utcnow().isoformat()))}
    od["total"] = len(cleaned_entries)
    od["entry"] = cleaned_entries
    return od


@require_GET
@protected_resource()
def fhir_endpoint_search(request, fhir_resource):
    up = UserProfile.objects.get(user=request.resource_owner)
    # Without an ID this is a search operation and return a Bundle
    if fhir_resource not in settings.FHIR_PATIENT_API_RESOURCES_SUPPORTED:
        raise Http404("fhir_resource %s is not supported." % (fhir_resource))

    # Disallow patient search
    if fhir_resource == "Patient":
        return JsonResponse(patient_search_not_allowed_response())
    for k, v in request.GET.items():
        if k == "patient" and v != up.fhir_patient_id:
            raise Http404("Invalid patient ID.")
        elif k == "subject":
            raise Http404("Invalid subject ID.")
        elif k == "beneficiary":
            raise Http404("Invalid subject ID.")
    patient_reference = "Patient/%s" % (up.fhir_patient_id)
    query = {"$or": [{"patient.reference": patient_reference},
                     {"subject.reference": patient_reference},
                     {"beneficiary.reference": patient_reference}, ]}

    d = query_mongo(settings.PATIENT_ACCESS_MONGODB_DATABASE_NAME, fhir_resource, query=query)

    bundle = make_bundle(d)
    return JsonResponse(bundle)


def get_user(request):
    try:
        user = request.resource_owner
    except AttributeError:
        user = request.user
    return user


def get_crosswalk(request):
    user = get_user(request)
    cw = get_object_or_404(Crosswalk, user=user)
    return cw


def patient_search_not_allowed_response():
    oo_response = OrderedDict()
    oo_response["resourceType"] = "OperationOutcome"
    oo_response["text"] = OrderedDict((
        ('status', 'generated'),
        ('div', """<div xmlns=\"http://www.w3.org/1999/xhtml\"><h1>Operation Outcome</h1>
                                        <table border=\"0\"><tr><td style=\"font-weight: bold;\">ERROR</td><td>[]</td>
                                        <td><pre>Patient search is not allowed on this server.</pre></td>
                                        \n\t\t\t\t\t\n\t\t\t\t\n\t\t\t</tr>\n\t\t
                                        </table>\n\t</div>""")))

    oo_response["issue"] = OrderedDict((
        ('severity', 'error'),
        ('code', 'processing'),
        ('diagnostics', 'Patient search is not allowed on this server'),
    ))
    return oo_response
