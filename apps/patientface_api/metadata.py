
patient_facing_api_metadata_str =\
    """
    {
	"resourceType": "CapabilityStatement",
	"id": "oauth2org-patient-facing-api",
	"text": {
		"status": "generated",
		"div": "<div xmlns=http://www.w3.org/1999/xhtml><p>OAuth2org Capability Statement for Patient Facing API server</div>"
	},
	"name": "oauth2org-patient-facing-api",
	"status": "draft",
	"date": "2021-01-18",
	"publisher": "Transparent Health",
	"contact": [{
		"telecom": [{
			"system": "url",
			"value": "http://hl7.org/fhir"
		}]
	}],
	"description": "OAuth2org Capability Statement for Patient Facing API server",
	"kind": "capability",
	"software": {
		"name": "Patient-facing App running on top of oauth2.org Server"
	},
	"fhirVersion": "4.0.1",
	"format": [
		"json"
	],
	"rest": [{
		"mode": "server",
		"documentation": "Transparent Health Capability Statement for Patient Facing and APIs",
		"security":{
               "service":[
                  {
                     "coding":[
                        {
                           "system":"http://terminology.hl7.org/CodeSystem/restful-security-service",
                           "code":"SMART-on-FHIR",
                           "display":"SMART-on-FHIR"
                        }
                     ],
                     "text":"See http://docs.smarthealthit.org/"
                  }
               ],
               "description":"OAuth2 with SMART-on FHIR profile support. Authorization_code flow only to get access_token. Server rejects any unauthorized requests by returning an HTTP 401 unauthorized response code."
            },
		"resource": [{
				"type": "Patient",
				"interaction": [{
						"code": "read"
					},
					{
						"code": "search-type",
						"documentation": "When a client searches patients with no search criteria, they get a list of all patients they have access too. Servers may elect to offer additional search parameters, but this is not required"
					}
				]
			},
			{
				"type": "DocumentReference",
				"interaction": [{
						"code": "read"
					},
					{
						"code": "search-type"
					}
				],
				"searchParam": [{
					"name": "_id",
					"type": "token",
					"documentation": "_id parameter always supported. For the connectathon, servers may elect which search parameters are supported"
				}]
			},
			{
				"type": "Observation",
				"interaction": [{
						"code": "read"
					},
					{
						"code": "search-type"
					}
				],
				"searchParam": [{
					"name": "_id",
					"type": "token",
					"documentation": "Standard _id parameter"
				}]
			},

			{
				"type": "AllergyIntolerance",
				"interaction": [{
						"code": "read"
					},
					{
						"code": "search-type"
					}
				],
				"searchParam": [{
					"name": "_id",
					"type": "token",
					"documentation": "Standard _id parameter"
				}]
			},

			{
				"type": "Medication",
				"interaction": [{
						"code": "read"
					},
					{
						"code": "search-type"
					}
				],
				"searchParam": [{
					"name": "_id",
					"type": "token",
					"documentation": "Standard _id parameter"
				}]
			},

			{
				"type": "MedicationStatement",
				"interaction": [{
						"code": "read"
					},
					{
						"code": "search-type"
					}
				],
				"searchParam": [{
					"name": "_id",
					"type": "token",
					"documentation": "Standard _id parameter"
				}]
			},

			{
				"type": "MedicationOrder",
				"interaction": [{
						"code": "read"
					},
					{
						"code": "search-type"
					}
				],
				"searchParam": [{
					"name": "_id",
					"type": "token",
					"documentation": "Standard _id parameter"
				}]
			},

			{
				"type": "CarePlan",
				"interaction": [{
						"code": "read"
					},
					{
						"code": "search-type"
					}
				],
				"searchParam": [{
					"name": "_id",
					"type": "token",
					"documentation": "Standard _id parameter"
				}]
			},

			{
				"type": "Immunization",
				"interaction": [{
						"code": "read"
					},
					{
						"code": "search-type"
					}
				],
				"searchParam": [{
					"name": "_id",
					"type": "token",
					"documentation": "Standard _id parameter"
				}]
			},

			{
				"type": "Device",
				"interaction": [{
						"code": "read"
					},
					{
						"code": "search-type"
					}
				],
				"searchParam": [{
					"name": "_id",
					"type": "token",
					"documentation": "Standard _id parameter"
				}]
			},

			{
				"type": "Goal",
				"interaction": [{
						"code": "read"
					},
					{
						"code": "search-type"
					}
				],
				"searchParam": [{
					"name": "_id",
					"type": "token",
					"documentation": "Standard _id parameter"
				}]
			},

			{
				"type": "Claim",
				"interaction": [{
						"code": "read"
					},
					{
						"code": "search-type"
					}
				],
				"searchParam": [{
					"name": "_id",
					"type": "token",
					"documentation": "Standard _id parameter"
				}]
			},
			{
				"type": "Coverage",
				"interaction": [{
						"code": "read"
					},
					{
						"code": "search-type"
					}
				],
				"searchParam": [{
					"name": "_id",
					"type": "token",
					"documentation": "Standard _id parameter"
				}]
			},

			{
				"type": "ExplanationofBenefit",
				"interaction": [{
						"code": "read"
					},
					{
						"code": "search-type"
					}
				],
				"searchParam": [{
					"name": "_id",
					"type": "token",
					"documentation": "Standard _id parameter"
				}]
			},
			{
				"type": "Practitioner",
				"interaction": [{
						"code": "read"
					},
					{
						"code": "search-type"
					}
				],
				"searchParam": [{
					"name": "_id",
					"type": "token",
					"documentation": "Standard _id parameter"
				}]
			},
			{
				"type": "Condition",
				"interaction": [{
						"code": "read"
					},
					{
						"code": "search-type"
					}
				],
				"searchParam": [{
					"name": "_id",
					"type": "token",
					"documentation": "Standard _id parameter"
				}]
			},
			{
				"type": "DiagnosticReport",
				"interaction": [{
						"code": "read"
					},
					{
						"code": "search-type"
					}
				],
				"searchParam": [{
						"name": "_id",
						"type": "token",
						"documentation": "Standard _id parameter"
					},
					{
						"name": "service",
						"type": "token",
						"documentation": "which diagnostic discipline/department created the report"
					}
				]
			}
		]
	}]
    }
"""  # noqa: W191, E101, E501, E122
