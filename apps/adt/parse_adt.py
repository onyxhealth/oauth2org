#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Alan Viars

from collections import OrderedDict
import hl7
import argparse
import json


adt_names = OrderedDict()
adt_names["A01"] = "Admit/visit notification"
adt_names["A02"] = "Transfer a patient"
adt_names["A03"] = "Discharge/end visit"
adt_names["A04"] = "Register a patient"
adt_names["A05"] = "Pre-admit a patient"
adt_names["A06"] = "Change an outpatient to an inpatient"
adt_names["A08"] = "Update patient information"
adt_names["A10"] = "Patient arriving - tracking"
adt_names["A15"] = "Pending transfer"
adt_names["A28"] = "Add person information"
adt_names["A29"] = "Delete person information"
adt_names["A30"] = "Merge person information"
adt_names["A31"] = "Update person information"


def parse_id_adt(input_file):
    """Parse adt into sensible json-like object"""
    list_of_messages = []
    responses = []
    message = ""
    with open(input_file, "r") as fh:
        for line in fh:
            if len(line) == 1:
                list_of_messages.append(message)
                message = ""
            else:
                if not line.endswith('\r'):
                    line += "\r"
                message += line

    # print(list_of_messages[0])
    for m in list_of_messages:
        h = hl7.parse(m)
        message = OrderedDict()
        message["message"] = OrderedDict()

        if str(h.segment('MSH')[9][0][0]) == "ADT":
            adt_type = str(h.segment('MSH')[9][0][1])
        message["message"]['adt_type'] = adt_type
        message["message"]['adt_description'] = adt_names[adt_type]
        message["message"]["id"] = h.segment('MSH')[10][0]
        message["message"]["from_system"] = str(
            h.segment('MSH')[3][0]).replace('^', '-')
        message["message"]["from_location"] = str(
            h.segment('MSH')[4][0]).replace('^', '-')
        message["message"]["to_system"] = str(
            h.segment('MSH')[5][0]).replace('^', '-')
        message["message"]["to_location"] = str(
            h.segment('MSH')[6][0]).replace('^', '-')
        message["message"]['timestamp'] = h.segment('MSH')[7][0]

        rd = OrderedDict()
        rd['sub'] = h.segment('PID')[3][0][0][0]
        rd['issuer'] = h.segment('PID')[3][0][3][0]
        rd['given_name'] = h.segment('PID')[5][0][1][0]
        rd['family_name'] = h.segment('PID')[5][0][0][0]

        # phone
        try:
            rd['phone_number'] = h.segment('PID')[13][0][0][0]
        except IndexError:
            pass

        # language
        try:
            rd['language'] = h.segment('PID')[15][0]
        except IndexError:
            pass

        # marital status
        try:
            rd['marital_status'] = h.segment('PID')[16][0][0][0]
        except IndexError:
            pass

        if h.segment('PID')[8] == "M":
            rd['gender'] = "male"
        elif h.segment('PID')[8] == "F":
            rd['gender'] = "female"

        rd['birthdate'] = h.segment('PID')[7][0]

        rd['address'] = []
        rd['document'] = []
        addr = OrderedDict()
        if len(h.segment('PID')[11][0]):
            addr['formatted'] = "%s %s %s %s %s %s" % (h.segment('PID')[11][0][0],
                                                       h.segment('PID')[
                11][0][1],
                h.segment('PID')[
                11][0][2],
                h.segment('PID')[11][0][3],
                h.segment('PID')[11][0][4],
                h.segment('PID')[11][0][5],
            )
            # Clean up the formatted address
            addr['formatted'] = addr['formatted'].strip()

            if len(h.segment('PID')[11][0][0]):
                addr['street_address'] = h.segment('PID')[11][0][0][0]

            if len(h.segment('PID')[11][0][1][0]):
                addr['street_address'] = "%s %s" % (
                    addr['street_address'], h.segment('PID')[11][0][1])
            addr['locality'] = h.segment('PID')[11][0][2][0]
            addr['region'] = h.segment('PID')[11][0][3][0]
            addr['postal_code'] = h.segment('PID')[11][0][4][0]
            addr['country'] = h.segment('PID')[11][0][5][0]
            if len(h.segment('PID')[11][0]) > 8:
                addr['county'] = h.segment('PID')[11][0][8][0]

        rd['address'].append(addr)

        doc = OrderedDict()
        doc['number'] = h.segment('PID')[3][0][0][0]
        doc['issuer'] = h.segment('PID')[3][0][3][0]
        doc['issuer_meta'] = []
        doc['issuer_meta'].append(h.segment('PID')[3][0][4][0])
        doc['issuer_meta'].append(h.segment('PID')[3][0][2][0])
        rd['document'].append(doc)

        # if an ssn was found, add it to the document claim
        # ssn
        try:
            ssn = h.segment('PID')[19][0]
            if ssn:
                doc = OrderedDict()
                doc['number'] = ssn
                doc['issuer'] = "Social Security Administration"
                doc['issuer_meta'] = []
                doc['issuer_meta'].append(
                    {"name": "ssn", "verbose_name": "Social Secuirity Number"})
                rd['document'].append(doc)
        except IndexError:
            pass

        message["patient_identity"] = rd
        responses.append(message)

    return responses


if __name__ == "__main__":

    # Parse args
    parser = argparse.ArgumentParser(description='Load in ADT stream.')
    parser.add_argument(
        dest='input_file',
        action='store',
        help='Input the ADT source file.')
    args = parser.parse_args()
    result = parse_id_adt(args.input_file)

    # output the JSON transaction summary
    print(json.dumps(result, indent=4))
