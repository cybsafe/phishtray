import uuid

from django.urls import reverse
from djangorestframework_camel_case.util import underscoreize
from rest_framework import status

from participant.models import ActionLog, Participant
from participant.serializer import ParticipantSerializer
from phishtray.test.base import PhishtrayAPIBaseTest
from ..factories import (
    ParticipantFactory,
    ParticipantActionFactory,
    ProfileEntryFactory,
    ActionLogFactory,
)
from exercise.factories import DemographicsInfoFactory, EmailFactory, ExerciseFactory
from rest_framework.test import APITestCase
from exercise.models import EXERCISE_EMAIL_PHISH, EXERCISE_EMAIL_REGULAR


class ParticipantAPITests(PhishtrayAPIBaseTest):
    def test_participant_list_block_public(self):
        """
        Non admin users should not be able to retrieve participant list.
        """
        url = reverse("api:participant-list")
        response = self.client.get(url)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_participant_list_allow_admin(self):
        """
        Admin users should be able to retrieve thread list.
        """
        url = reverse("api:participant-list")
        participant_count = 5
        ParticipantFactory.create_batch(participant_count)

        response = self.admin_client.get(url)
        serialized = ParticipantSerializer(Participant.objects.all(), many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(participant_count, len(response.data))
        self.assertEqual(serialized.data, underscoreize(response.data))

    def test_participant_details(self):
        """
        Participant details are public.
        """
        participants_count = 2
        ParticipantFactory.create_batch(participants_count)
        participant = ParticipantFactory()

        # Actions
        actions_count = 2
        ParticipantActionFactory.create_batch(actions_count, participant=participant)

        # Profile Entries
        profile_entries_count = 2
        profile_entries = ProfileEntryFactory.create_batch(profile_entries_count)
        participant.profile.add(*profile_entries)
        participant.save()

        url = reverse("api:participant-detail", args=[participant.id])
        response = self.admin_client.get(url)
        serialized = ParticipantSerializer(Participant.objects.get(pk=participant.id))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serialized.data, underscoreize(response.data))
        self.assertEqual(actions_count, len(response.data.get("actions")))
        self.assertEqual(profile_entries_count, len(response.data.get("profile")))

    def test_get_participant_details_404(self):
        fake_id = "fakeID"
        url = reverse("api:participant-detail", args=[fake_id])

        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual("Not found.", response.data.get("detail"))


class ParticipantProfileAPITests(PhishtrayAPIBaseTest):
    def setUp(self):
        super().setUp()
        self.participant = ParticipantFactory()
        # create questions and profile entries
        self.questions = DemographicsInfoFactory.create_batch(5)
        self.participant.exercise.demographics.add(*self.questions)
        self.participant.save()

    def test_update_participant_profile(self):
        url = reverse("api:participant-extend_profile", args=[self.participant.id])
        data = {
            "profileForm": [
                {"id": self.questions[0].id, "value": "20"},
                {"id": self.questions[2].id, "value": "Some text"},
            ]
        }

        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            "Participant profile has been successfully updated.",
            response.data.get("message"),
        )
        self.assertEqual(2, self.participant.profile.all().count())

    def test_partial_update_participant_profile(self):
        url = reverse("api:participant-extend_profile", args=[self.participant.id])
        bad_id_1 = str(uuid.uuid4())
        bad_id_2 = str(uuid.uuid4())
        data = {
            "profileForm": [
                {"id": bad_id_1, "value": "20"},
                {"id": bad_id_2, "value": "wibble wobble"},
                {"id": self.questions[2].id, "value": "Some text"},
            ]
        }

        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            "Participant profile has been partially updated due to errors.",
            response.data.get("message"),
        )
        self.assertEqual(
            "Missing or invalid demographics IDs.",
            response.data["errors"][0]["message"],
        )
        self.assertListEqual(
            [bad_id_1, bad_id_2], response.data["errors"][0]["id_list"]
        )
        self.assertEqual(1, self.participant.profile.all().count())

    def test_update_participant_profile_missing_profile_form_data(self):
        url = reverse("api:participant-extend_profile", args=[self.participant.id])
        data = {
            # Note the spelling mistake / mismatch
            "profileFromOops": [
                {"id": self.questions[0].id, "value": "20"},
                {"id": self.questions[2].id, "value": "Some text"},
            ]
        }

        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(0, self.participant.profile.all().count())


class ParticipantActionsAPITests(PhishtrayAPIBaseTest):
    def setUp(self):
        super().setUp()
        self.participant = ParticipantFactory()

    def test_add_participant_action(self):
        url = reverse("api:participant-action", args=[self.participant.id])
        data = {
            "action_type": "SOME_ACTION_TYPE",
            "key1": 1234,
            "key2": "some value",
            "key3": "wibble wobble",
        }

        response = self.client.post(url, data)
        action_id = response.data.get("action_id")

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            "Action has been logged successfully.", response.data.get("message")
        )
        self.assertEqual(4, ActionLog.objects.filter(action__id=action_id).count())

    def test_add_participant_action_skip_complex_datatypes(self):
        url = reverse("api:participant-action", args=[self.participant.id])
        data = {
            "action_type": "SOME_ACTION_TYPE",
            "key1": 1234,
            "key2": "some value",
            "just_a_list": ["t", "e", "s", "t"],
            "just_a_dict": {"wibble": 1, "wobble": 2, "another_list": [1, 2, 3, 4]},
        }

        response = self.client.post(url, data)
        action_id = response.data.get("action_id")

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            "Action has been partially logged. Cannot log complex data types.",
            response.data.get("message"),
        )
        self.assertListEqual(
            ["just_a_list", "just_a_dict"], response.data.get("skipped")
        )
        self.assertEqual(3, ActionLog.objects.filter(action__id=action_id).count())

    def test_add_participant_action_convert_keys_to_snake_case(self):
        url = reverse("api:participant-action", args=[self.participant.id])
        data = {
            "actionType": "SOME_ACTION_TYPE",
            "myKeyOne": 1234,
            "mix_andMatch": "wobble",
        }
        expected_keys = ["action_type", "my_key_one", "mix_and_match"]

        response = self.client.post(url, data)
        action_id = response.data.get("action_id")
        action_names = [
            al.name for al in ActionLog.objects.filter(action__id=action_id)
        ]

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            "Action has been logged successfully.", response.data.get("message")
        )
        self.assertEqual(3, ActionLog.objects.filter(action__id=action_id).count())
        self.assertListEqual(sorted(expected_keys), sorted(action_names))

    def test_add_participant_action_nothing_to_log(self):
        url = reverse("api:participant-action", args=[self.participant.id])
        data = {}

        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("Nothing to log.", response.data.get("message"))


class ParticipantScoresAPI(APITestCase):
    def setUp(self):
        exercise = ExerciseFactory(
            debrief=True, training_link="https://app.cybsafe.com"
        )
        self.phishing_email_1 = EmailFactory(
            subject="Phishing Email", phish_type=EXERCISE_EMAIL_PHISH
        )
        self.phishing_email_2 = EmailFactory(
            subject="Phishing Email", phish_type=EXERCISE_EMAIL_PHISH
        )
        non_phishing_email = EmailFactory(
            subject="Non Phishing Email Test", phish_type=EXERCISE_EMAIL_REGULAR
        )
        exercise.emails.add(self.phishing_email_1)
        exercise.emails.add(non_phishing_email)
        exercise.emails.add(self.phishing_email_2)

        self.participant = ParticipantFactory(exercise=exercise)
        self.url = reverse("api:participant-score-detail", args=[self.participant.id])

    def test_participant_scores_debrief_has_only_phishing_emails(self):
        response = self.client.get(self.url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.data["phishing_emails"]))
        self.assertEqual("https://app.cybsafe.com", response.data["training_link"])
        self.assertEqual(True, response.data["debrief"])
        self.assertEqual(
            "Phishing Email", response.data["phishing_emails"][0]["subject"]
        )
        self.assertEqual(
            "Phishing Email", response.data["phishing_emails"][1]["subject"]
        )

    def test_participant_scores_debrief_behaviour_responses(self):
        test_data = [
            ["email_attachment_download", "negative"],
            ["email_reported", "positive"],
            ["something_not_postive_or_negative", "neutral"],
        ]

        for act, behaviour in test_data:
            with self.subTest(act=act, behaviour=behaviour):
                exercise = ExerciseFactory(debrief=True)
                phishing_email = EmailFactory(
                    subject="Phishing Email", phish_type=EXERCISE_EMAIL_PHISH
                )
                exercise.emails.add(phishing_email)

                participant = ParticipantFactory(exercise=exercise)
                url = reverse("api:participant-score-detail", args=[participant.id])

                action = ParticipantActionFactory(participant=participant)
                ActionLogFactory(
                    action=action, name="email_id", value=str(phishing_email.id)
                )
                ActionLogFactory(action=action, name="action_type", value=act)

                response = self.client.get(url)
                self.assertEqual(status.HTTP_200_OK, response.status_code)
                self.assertEqual(1, len(response.data["phishing_emails"]))
                self.assertEqual(
                    1, len(response.data["phishing_emails"][0]["participant_actions"])
                )
                self.assertEqual(
                    behaviour,
                    response.data["phishing_emails"][0]["participant_behaviour"][
                        "behaviour"
                    ],
                )
                if behaviour == "neutral":
                    self.assertIsNone(
                        response.data["phishing_emails"][0]["participant_behaviour"][
                            "action_id"
                        ]
                    )
                else:
                    self.assertEqual(
                        str(action.id),
                        response.data["phishing_emails"][0]["participant_behaviour"][
                            "action_id"
                        ],
                    )
