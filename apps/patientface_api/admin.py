from django.contrib import admin
from .models import Crosswalk


class CrosswalkAdmin(admin.ModelAdmin):
    list_display = ('user', 'fhir_patient_id', 'issuer',)
    search_fields = ('user', 'fhir_patient_id', 'issuer',)
    raw_id_fields = ("user", )


admin.site.register(Crosswalk, CrosswalkAdmin)
