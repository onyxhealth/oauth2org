from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

# Copyright Videntity Systems Inc.


__author__ = "Alan Viars"


class Crosswalk(models.Model):
    """
    User to FHIR Patient ID Crosswalk/Mapping
    """
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=True)
    fhir_source = models.TextField(default=settings.DEFAULT_FHIR_SERVER,
                                   blank=True)
    issuer = models.TextField(blank=True, default="",
                              help_text=_("Usually an URL"))
    fhir_patient_id = models.CharField(max_length=255,
                                       blank=True, default="",
                                       db_index=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user_identifier = models.CharField(max_length=255, blank=True,
                                       default="")
    user_id_type = models.CharField(max_length=255,
                                    default="", blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.user_identifier

    def patient_fhir_url(self):
        fhir_endpoint = "%sPatient/%s" % (self.fhir_source,
                                          self.fhir_patient_id)
        return fhir_endpoint

    class Meta:
        unique_together = (("user", "user_identifier", "issuer"),)
