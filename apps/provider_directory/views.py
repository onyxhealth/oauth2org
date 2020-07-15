from django.shortcuts import render
from .mongoutils import query_mongo
from collections import OrderedDict
import uuid
from django.http import HttpResponse
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
    
    query = dict(request.GET)
    
    if 'family' in query.keys():
      query['name.family'] = query['family']
      del query['family']
      
    if 'given' in query.keys():
      query['name.given'] = query['given']
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
  query = dict(request.GET)
  if 'identifier' in query.keys():
      query['identifier.coding.value'] = query['identifier']
      del query['identifier']
  if '_id' in query.keys():
      query['id'] = query['_id']
      del query['_id']
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
    return HttpResponse(json.dumps(q['results'][0], indent=4),
                            content_type="application/json+fhir")
    

def organization_fhir_read(request, id):
    q = query_mongo(database_name="fhir4",
                collection_name="Organization",
                query={'id': id})
    return HttpResponse(json.dumps(q['results'][0], indent=4),
                            content_type="application/json+fhir")