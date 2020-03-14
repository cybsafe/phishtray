from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from inline_actions.admin import InlineActionsModelAdminMixin

from .models import Participant, Organization
from .filters import TrialVersionListFilter, ExerciseListFilter
from .helpers import ExportCSVMixinHelpers
from django.http import HttpResponse

import csv


class ExportCsvMixin:
    def download_csv(self, request, queryset):

        meta = self.model._meta

        exercise_ids = queryset.values_list("exercise_id")

        csv_columns, csv_rows = ExportCSVMixinHelpers().get_participant_stats_csv_data(
            exercise_ids
        )

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)

        writer.writerow(csv_columns)
        for obj in csv_rows:
            writer.writerow([obj[field] for field in csv_columns])

        return response

    download_csv.short_description = "Download Selected CSV"


class EmailCSV:
    inline_actions = ["email_csv"]

    def email_csv(self, request, obj, parent_obj=None):
        """Download CSV using the API endpoint"""
        uri = f"{reverse('api:exercise-report-detail', args=[obj.exercise.pk])}download-csv?participant={obj.pk}"
        return redirect(uri)

    email_csv.short_description = "⬇ Email Interactions CSV"


@admin.register(Participant)
class ParticipantList(
    EmailCSV, InlineActionsModelAdminMixin, admin.ModelAdmin, ExportCsvMixin
):
    list_filter = (ExerciseListFilter, TrialVersionListFilter)
    list_display = ("id", "exercise")
    actions = ["download_csv"]
    readonly_fields = (
        "exercise",
        "profile",
        "organization",
    )

    def get_queryset(self, request):
        return Participant.objects.filter_by_user(user=request.user)

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_filter = ("name",)
    list_display = ("id", "name")

    def get_queryset(self, request):
        return Organization.objects.filter_by_user(user=request.user)

    def has_add_permission(self, request):
        if not request.user.is_superuser:
            return False

        return super().has_add_permission(request)
