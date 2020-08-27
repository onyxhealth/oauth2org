#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Alan Viars

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.decorators import protected_resource
from .parse_adt import parse_id_adt
import uuid
import os
import json
from collections import OrderedDict


@protected_resource
@csrf_exempt
def post_adt_feed(request):
    if request.method == 'POST':
        # file name
        temp_filename = "%s.txt" % (uuid.uuid4())
        body_ascii = request.body.decode('ascii')
        tmpfile = open(temp_filename, "w")
        tmpfile.writelines(body_ascii)
        tmpfile.close()
        r = parse_id_adt(temp_filename)

        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        results = OrderedDict()
        results["results"] = r
        results["total"] = len(r)
        return HttpResponse(json.dumps(results, indent=4))
    return HttpResponse("POST an ADT message feed as the BODY")
