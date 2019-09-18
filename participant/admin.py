from django.contrib import admin
from .models import Participant
from django.http import HttpResponse
import csv


class ExportCsvMixin:
    def download_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    download_csv.short_description = "Download Selected CSV"


@admin.register(Participant)
class ParticipantList(admin.ModelAdmin, ExportCsvMixin):
    list_filter = ("exercise",)
    actions = ["download_csv"]
