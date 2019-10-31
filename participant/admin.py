from django.contrib import admin
from .models import Participant, Organization
from .filters import TrialVersionListFilter
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
    list_filter = ("exercise", TrialVersionListFilter)
    actions = ["download_csv"]

    def get_queryset(self, request):
        return Participant.objects.filter_by_user(user=request.user)

    def has_add_permission(self, request):
        if not request.user.is_superuser:
            return False

        return super().has_add_permission(request)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_filter = ("name",)
    list_display = ("id", "name")
