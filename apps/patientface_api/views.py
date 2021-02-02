from django.http import JsonResponse, Http404
from collections import OrderedDict
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.views.decorators.http import require_GET
from oauth2_provider.decorators import protected_resource
from .models import Crosswalk
from .mongo_utils import query_mongo
from bson import ObjectId
from .metadata import patient_facing_api_metadata_str
import json
from ..accounts.models import UserProfile


__author__ = "Alan Viars"


FHIR_RESOURCE_TO_ID_MAP = OrderedDict()
FHIR_RESOURCE_TO_ID_MAP['Patient'] = ""
FHIR_RESOURCE_TO_ID_MAP['Observation'] = "subject"
FHIR_RESOURCE_TO_ID_MAP['Condition'] = "subject"
FHIR_RESOURCE_TO_ID_MAP['AllergyIntolerance'] = "patient"
FHIR_RESOURCE_TO_ID_MAP['Medication'] = ""
FHIR_RESOURCE_TO_ID_MAP['MedicationStatement'] = "patient"
FHIR_RESOURCE_TO_ID_MAP['MedicationOrder'] = ""
FHIR_RESOURCE_TO_ID_MAP['DiagnosticReport'] = "patient"
FHIR_RESOURCE_TO_ID_MAP['Procedure'] = "patient"
FHIR_RESOURCE_TO_ID_MAP['CarePlan'] = "patient"
FHIR_RESOURCE_TO_ID_MAP['Immunization'] = "patient"
FHIR_RESOURCE_TO_ID_MAP['Device'] = "patient"
FHIR_RESOURCE_TO_ID_MAP['Goal'] = "patient"
FHIR_RESOURCE_TO_ID_MAP['ExplanationOfBenefit'] = "patient"
FHIR_RESOURCE_TO_ID_MAP['Coverage'] = ""


@require_GET
def fhir_metadata_endpoint(request):
    return JsonResponse(json.loads(patient_facing_api_metadata_str, object_pairs_hook=OrderedDict))


@require_GET
@protected_resource()
def fhir_endpoint_with_id(request, fhir_resource, id):

    if fhir_resource not in settings.FHIR_RESOURCES_SUPPORTED:
        raise Http404

    up = UserProfile.objects.get(user=request.resource_owner) 
    if up.fhir_patient_id != id and fhir_resource == "Patient":
        # Do not allow mismatched token/user/fhir ID
        raise Http404

    d = query_mongo("qhn-fhir4", fhir_resource, query={"id": id}, limit=1)

    if not d["results"]:
        d = query_mongo("qhn-fhir4", fhir_resource, query={"id": ObjectId(id)}, limit=1)
    
    if not d["results"]:
        d = query_mongo("qhn-fhir4", fhir_resource, query={"_id": id}, limit=1) 

    if not d["results"]:
        d = query_mongo("qhn-fhir4", fhir_resource, query={"_id": ObjectId(id)}, limit=1) 
    if not d["results"]:
        raise Http404
    one_result = d["results"][0]

    if "_id" in one_result.keys():
        if isinstance(one_result["_id"], ObjectId):
            one_result["_id"] = str(one_result["_id"])

    if "id" in one_result.keys():
        if isinstance(one_result["id"], ObjectId):
            one_result["id"] = str(one_result["id"])

    # Return only a single FHIR Resource
    return JsonResponse(one_result)


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
