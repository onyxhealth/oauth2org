from django.shortcuts import render
from .mongoutils import query_mongo
from collections import OrderedDict
import uuid
from django.http import HttpResponse, Http404
import json

# Copyright Videntity Systems, Inc. 2020

def format_search_result(entry):
  stub = OrderedDict()
  stub["resourceType"]= "Bundle"
  stub["id"]= str(uuid.uuid4())
  stub["type"] ="searchset"
  stub["total"] = len(entry)
  stub["entry"]= entry
  return stub

def practitioner_fhir_search(request):
    
    query = dict(request.GET.items())
    
  
    if 'address-postalcode' in query.keys():
      query['address.postalCode'] = query['address-postalcode']
      del query['address-postalcode']
 
    if 'address-state' in query.keys():
      query['address.state'] = query['address-state'].upper()
      del query['address-state']
    
    if 'family' in query.keys():
      query['name.family'] = query['family'].upper()
      del query['family']
      
    if 'given' in query.keys():
      query['name.given'] = query['given'].upper()
      del query['given']
  
    if 'identifier' in query.keys():
      query['identifier.value'] = query['identifier']
      del query['identifier']
  
    if '_id' in query.keys():
      query['id'] = query['_id']
      del query['_id']
  
    q = query_mongo(database_name="fhir4",
                collection_name="Practitioner",
                limit=2,
                query=query
                )
    response = format_search_result(q['results'])
    return HttpResponse(json.dumps(response, indent=4),
                            content_type="application/json+fhir")
    

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


  q = query_mongo(database_name="fhir4",
                collection_name="Organization",
                limit=2,
                query=query
                )
  response = format_search_result(q['results'])
  return HttpResponse(json.dumps(response, indent=4),
                            content_type="application/json+fhir")
    

def practitioner_fhir_read(request, id):
    q = query_mongo(database_name="fhir4",
                collection_name="Practitioner",
                query={'id': id})
    if q['results']:
        return HttpResponse(json.dumps(q['results'][0], indent=4),
                            content_type="application/json+fhir")
    else:
      raise Http404
    

def organization_fhir_read(request, id):
    q = query_mongo(database_name="fhir4",
                collection_name="Organization",
                query={'id': id})
    if q['results']:
        return HttpResponse(json.dumps(q['results'][0], indent=4),
                            content_type="application/json+fhir")
    else:
      raise Http404