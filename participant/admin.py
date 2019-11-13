from django.contrib import admin
from .models import Participant, Organization, ParticipantAction, ActionLog
from .serializer import ParticipantActionSerializer
from .filters import TrialVersionListFilter, ExerciseListFilter
from django.http import HttpResponse
from django.db.models import (
    F,
    Q,
    Value,
    CharField,
    OuterRef,
    Subquery,
    ExpressionWrapper,
    Case,
    When,
    Count,
)
from django.db.models.functions import Coalesce, Concat, Now
from exercise.models import Exercise
import csv


class ExportCsvMixin:
    def download_csv(self, request, queryset):

        meta = self.model._meta

        exercise_ids = queryset.values_list("exercise_id")

        # Steps:
        # 1 - Get the exercises from the selected participant(s)
        exercise_qs = Exercise.objects.filter(id__in=exercise_ids)

        # 2 - Calculate the results based on the actual exercises
        exercise_participants_qs = (
            Participant.objects.filter(exercise_id=OuterRef("pk"))
            .values("exercise_id")
            .annotate(participant_count=Count("exercise_id"))
        )

        participant_actions_qs = (
            ActionLog.objects.filter(action__participant__exercise_id=OuterRef("pk"))
            .values("action__participant__exercise_id")
            .annotate(
                dcount=Count("action__participant__exercise_id"),
                emails_opened=Count(
                    "id", filter=Q(name="action_type", value="email_opened")
                ),
                emails_reported=Count(
                    "id", filter=Q(name="action_type", value="email_reported")
                ),
                emails_deleted=Count(
                    "id", filter=Q(name="action_type", value="email_deleted")
                ),
                emails_linked_click=Count(
                    "id", filter=Q(name="action_type", value="email_link_clicked")
                ),
                clicked_training_link=Count(
                    "id", filter=Q(name="action_type", value="training_link_clicked")
                ),
                email_opened_attachment=Count(
                    "id",
                    filter=Q(name="action_type", value="email_attachment_download"),
                )
                # refresher_failed=Coalesce(
                #     Count("id", filter=Q(is_passed=0), distinct=True), 0
                # ),
            )
        )

        #   fileDelete: 'file_deleted',
        #   fileOpen: 'file_opened',
        #   emailOpen: 'email_opened',
        #   emailReply: 'email_replied',
        #   emailForward: 'email_forwarded',
        #   emailDelete: 'email_deleted',
        #   emailReport: 'email_reported',
        #   emailQuickReply: 'email_quick_reply',
        #   emailAttachmentDownload: 'email_attachment_download',
        #   emailLinkOpen: 'email_link_clicked',
        #   accountOpen: 'account_open',
        #   contactOpen: 'contact_open',
        #   browserClose: 'browser_closed',
        #   browserClick: 'webpage_click',
        #   browserInputChange: 'webpage_entry',
        #   browserInputLoginCrendentials: 'webpage_login_credentials_entered',
        #   browserForgottenPassword: 'webpage_forgotten_password',
        #   browserSubmittedDetails: 'webpage_login_credentials_submitted',
        #   browserUserSignUp: 'webpage_user_signup',
        #   trainingLinkClick: 'training_link_clicked',

        # 3 - Organize the results to show on CSV

        # participant_actions_queryset = ParticipantAction.objects.filter(
        #     participant_id=participant_id
        # )
        # serialized_actions = ParticipantActionSerializer(
        #     participant_actions_queryset, many=True
        # )
        #
        # # print(f"Result: {str(serialized_actions, 'utf-8')}")
        # print(serialized_actions)

        field_names = [
            "exercise_title",
            "exercise_trial_version",
            "emails_opened",
            "phishing_emails_opened",
            "pos_reported",
            "pos_deleted",
            "neg_clicked_link",
            "neg_entered_detail",
            "neg_replied_to_phishing_email",
            "neg_opened_attachment",
            "participant_count",
            "training_link_clicked",
        ]

        queryset = exercise_qs.annotate(
            exercise_title=F("title"),
            exercise_trial_version=F("trial_version"),
            emails_opened=Coalesce(
                Subquery(
                    participant_actions_qs.values("emails_opened")[:1],
                    output_field=CharField(),
                ),
                0,
            ),
            phishing_emails_opened=Value("", output_field=CharField()),
            pos_reported=Subquery(
                participant_actions_qs.values("emails_reported")[:1],
                output_field=CharField(),
            ),
            pos_deleted=Subquery(
                participant_actions_qs.values("emails_deleted")[:1],
                output_field=CharField(),
            ),
            neg_clicked_link=Subquery(
                participant_actions_qs.values("emails_linked_click")[:1],
                output_field=CharField(),
            ),
            neg_entered_detail=Value("", output_field=CharField()),
            neg_replied_to_phishing_email=Value("", output_field=CharField()),
            neg_opened_attachment=Subquery(
                participant_actions_qs.values("email_opened_attachment")[:1],
                output_field=CharField(),
            ),
            participant_count=Subquery(
                exercise_participants_qs.values("participant_count")[:1],
                output_field=CharField(),
            ),
            training_link_clicked=Coalesce(
                Subquery(
                    participant_actions_qs.values("clicked_training_link")[:1],
                    output_field=CharField(),
                ),
                Value("N.A."),
            ),
        )

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            # print([getattr(obj, field) for field in field_names])
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    download_csv.short_description = "Download Selected CSV"


@admin.register(Participant)
class ParticipantList(admin.ModelAdmin, ExportCsvMixin):
    list_filter = (ExerciseListFilter, TrialVersionListFilter)
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
