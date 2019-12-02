from django.db.models import (
    Q,
    CharField,
    OuterRef,
    Subquery,
    Count,
    Case,
    When,
    Value,
    F,
)
from django.db.models.functions import Coalesce

from .serializer import ParticipantActionSerializer
from .models import Participant, ParticipantAction

from exercise import models as exercise_models


class ExportCSVMixinHelpers:
    def get_participant_stats_csv_data(self, exercise_ids):

        exercise_qs = exercise_models.Exercise.objects.filter(id__in=exercise_ids)

        email_type_count_map = self.get_emails_count_map(exercise_qs)

        exercise_participants_qs = (
            Participant.objects.filter(exercise_id=OuterRef("pk"))
            .values("exercise_id")
            .annotate(participant_count=Count("exercise_id"))
        )

        participant_actions_qs = (
            ParticipantAction.objects.filter(participant__exercise_id=OuterRef("pk"))
            .values("participant__exercise_id")
            .annotate(
                dcount=Count("participant__exercise_id"),
                emails_reported=self.get_action_count("email_reported"),
                emails_deleted=self.get_action_count("email_deleted"),
                emails_linked_click=self.get_action_count("email_link_clicked"),
                clicked_training_link=Case(
                    When(
                        participant__exercise__debrief=True,
                        then=(self.get_action_count("training_link_clicked")),
                    )
                ),
                email_opened_attachment=self.get_action_count(
                    "email_attachment_download"
                ),
                webpage_clicked=self.get_action_count("webpage_click"),
                emails_replied=self.get_action_count("email_replied"),
                code_skipped=self.get_action_count("training_release_code_skipped"),
                code_correct=self.get_action_count("training_release_code_correct"),
                code_incorrect=self.get_action_count("training_release_code_incorrect"),
            )
        )

        csv_columns = [
            "title",
            "trial_version",
            "emails_opened",
            "phishing_emails_opened",
            "pos_reported",
            "pos_deleted",
            "neg_clicked_link",
            "neg_entered_detail",
            "neg_replied_to_phishing_email",
            "neg_opened_attachment",
            "code_entered",
            "code_skipped",
            "code_correct",
            "code_incorrect",
            "participant_count",
            "training_link_clicked",
        ]

        rows_qs = exercise_qs.annotate(
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
            code_skipped=Coalesce(
                self.get_subquery_value(participant_actions_qs, "code_skipped"), 0
            ),
            code_correct=Coalesce(
                self.get_subquery_value(participant_actions_qs, "code_correct"), 0
            ),
            code_incorrect=Coalesce(
                self.get_subquery_value(participant_actions_qs, "code_incorrect"), 0
            ),
            code_entered=Coalesce(F("code_correct") + F("code_incorrect"), 0),
            participant_count=self.get_subquery_value(
                exercise_participants_qs, "participant_count"
            ),
            training_link_clicked=Coalesce(
                self.get_subquery_value(
                    participant_actions_qs, "clicked_training_link"
                ),
                Value("N.A."),
            ),
        ).values(
            "id",
            "title",
            "trial_version",
            "pos_reported",
            "pos_deleted",
            "neg_clicked_link",
            "neg_entered_detail",
            "neg_replied_to_phishing_email",
            "neg_opened_attachment",
            "code_entered",
            "code_skipped",
            "code_correct",
            "code_incorrect",
            "participant_count",
            "training_link_clicked",
        )

        csv_rows = list(rows_qs)

        for row in csv_rows:
            row["emails_opened"] = email_type_count_map[row["id"]]["regular_emails"]
            row["phishing_emails_opened"] = email_type_count_map[row["id"]][
                "phishing_emails"
            ]

        return csv_columns, csv_rows

    @staticmethod
    def get_subquery_value(queryset, value):
        return Subquery(queryset.values(value)[:1], output_field=CharField())

    @staticmethod
    def get_action_count(action):
        return Count(
            "id", filter=Q(actionlog__name="action_type", actionlog__value=action)
        )

    @staticmethod
    def get_emails_count_map(exercise_qs):
        emails_count_map = {}
        for exercise in exercise_qs:
            # Participants actions based on the exercise
            participant_actions_queryset = ParticipantAction.objects.filter(
                participant__exercise=exercise
            )
            # serializing actions to filter only the ones corresponding to emails opened
            serialized_actions = ParticipantActionSerializer(
                participant_actions_queryset, many=True
            ).data

            # Filtering email opened ids
            email_uuids = {
                action["action_details"]["email_id"]
                for action in serialized_actions
                if (action["action_details"].get("email_id"))
                and (action["action_details"].get("action_type") == "email_opened")
            }

            # Getting opened emails to verify if they are phishing or regular ones
            exercise_scoped_emails = exercise_models.ExerciseEmail.objects.filter(
                id__in=email_uuids
            )

            phishing_emails_count = exercise_scoped_emails.filter(
                phish_type=exercise_models.EXERCISE_EMAIL_PHISH
            ).count()

            regular_emails_count = exercise_scoped_emails.filter(
                phish_type=exercise_models.EXERCISE_EMAIL_REGULAR
            ).count()

            emails_count_map[exercise.id] = {
                "phishing_emails": phishing_emails_count,
                "regular_emails": regular_emails_count,
            }

        return emails_count_map
