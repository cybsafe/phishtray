from django.db.models import F, Q, Value, CharField, OuterRef, Subquery, Count
from django.db.models.functions import Coalesce

from exercise.models import Exercise
from .models import Participant, ActionLog


class ExportCSVMixinHelpers:
    def get_participant_stats_csv_data(self, exercise_ids):

        exercise_qs = Exercise.objects.filter(id__in=exercise_ids)

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
                emails_opened=self.get_action_count("email_opened"),
                emails_reported=self.get_action_count("email_reported"),
                emails_deleted=self.get_action_count("email_deleted"),
                emails_linked_click=self.get_action_count("email_link_clicked"),
                clicked_training_link=self.get_action_count("training_link_clicked"),
                email_opened_attachment=self.get_action_count(
                    "email_attachment_download"
                ),
                webpage_clicked=self.get_action_count("webpage_click"),
                emails_replied=self.get_action_count("email_replied"),
            )
        )

        csv_columns = [
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

        csv_rows = exercise_qs.annotate(
            exercise_title=F("title"),
            exercise_trial_version=F("trial_version"),
            emails_opened=Coalesce(
                self.get_subquery_value(participant_actions_qs, "emails_opened"), 0
            ),
            phishing_emails_opened=Value(0, output_field=CharField()),
            pos_reported=Coalesce(
                self.get_subquery_value(participant_actions_qs, "emails_reported"), 0
            ),
            pos_deleted=Coalesce(
                self.get_subquery_value(participant_actions_qs, "emails_deleted"), 0
            ),
            neg_clicked_link=Coalesce(
                self.get_subquery_value(participant_actions_qs, "emails_linked_click"),
                0,
            ),
            neg_entered_detail=Coalesce(
                self.get_subquery_value(participant_actions_qs, "webpage_clicked"), 0
            ),
            neg_replied_to_phishing_email=Coalesce(
                self.get_subquery_value(participant_actions_qs, "emails_replied"), 0
            ),
            neg_opened_attachment=Coalesce(
                self.get_subquery_value(
                    participant_actions_qs, "email_opened_attachment"
                ),
                0,
            ),
            participant_count=self.get_subquery_value(
                exercise_participants_qs, "participant_count"
            ),
            training_link_clicked=self.get_subquery_value(
                participant_actions_qs, "clicked_training_link"
            ),
        )

        return csv_columns, csv_rows

    @staticmethod
    def get_subquery_value(queryset, value):
        return Subquery(queryset.values(value)[:1], output_field=CharField())

    @staticmethod
    def get_action_count(action):
        return Count("id", filter=Q(name="action_type", value=action))
