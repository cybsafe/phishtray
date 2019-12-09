from random import randint

from django.db.models import F
from django.urls import reverse
from rest_framework.views import status
from djangorestframework_camel_case.util import underscoreize

from participant.factories import ParticipantFactory, ProfileEntryFactory
from phishtray.test.base import PhishtrayAPIBaseTest, ThreadTestsMixin
from ..models import Exercise, ExerciseEmail, ExerciseEmailProperties
from ..serializer import ExerciseSerializer, ExerciseEmailSerializer, ThreadSerializer
from ..factories import (
    ExerciseFileFactory,
    EmailFactory,
    EmailReplyFactory,
    ExerciseFactory,
    DemographicsInfoFactory,
    ExerciseWebPageReleaseCodeFactory,
    ExerciseWebPageFactory,
)


class ExerciseAPITests(PhishtrayAPIBaseTest, ThreadTestsMixin):
    def test_exercise_list_block_public(self):
        """
        Non admin users should not be able to retrieve the exercise list.
        """
        url = reverse("api:exercise-list")
        response = self.client.get(url)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_exercise_list_allow_admin(self):
        """
        Admin users should be able to retrieve the exercise list.
        """
        url = reverse("api:exercise-list")
        exercises_count = 3
        ExerciseFactory.create_batch(exercises_count)

        response = self.admin_client.get(url)
        serialized = ExerciseSerializer(Exercise.objects.all(), many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(exercises_count, len(response.data))
        self.assertEqual(serialized.data, underscoreize(response.data))

    def test_get_exercise_details(self):
        """
        Exercise details are public.
        """
        exercise_1 = ExerciseFactory()
        # add emails
        email_count = 3
        emails = EmailFactory.create_batch(email_count)
        self.threadify(emails[0])
        self.threadify(emails[1])
        exercise_1.emails.add(*emails)
        # add files
        file_count = 2
        files = ExerciseFileFactory.create_batch(file_count)
        exercise_1.files.add(*files)
        exercise_1.save()

        url = reverse("api:exercise-detail", args=[exercise_1.id])

        response = self.client.get(url)
        serialized = ExerciseSerializer(Exercise.objects.get(pk=exercise_1.id))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.data.get("threads")))
        self.assertEqual(file_count, len(response.data.get("files")))
        self.assertEqual(serialized.data, underscoreize(response.data))

    def test_get_exercise_details_404(self):
        """
        Exercise details are public.
        """
        fake_id = "fakeID"
        url = reverse("api:exercise-detail", args=[fake_id])

        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual("Not found.", response.data.get("detail"))

    def test_get_exercise_email_properties(self):
        emails = EmailFactory.create_batch(1)
        self.threadify(emails[0])
        exercise = ExerciseFactory.create(emails=emails)
        email_properties = ExerciseEmailProperties.objects.filter(
            exercise=exercise
        ).first()

        email_properties.web_page = ExerciseWebPageFactory(url="Test Page URL")
        email_properties.release_codes.add(
            ExerciseWebPageReleaseCodeFactory(release_code="Test Release Code")
        )
        email_properties.save()

        url = reverse("api:exercise-detail", args=[exercise.id])

        response = self.client.get(url)
        thread_properties = response.data.get("threads")[0]["thread_properties"]

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.data.get("threads")))
        self.assertEqual(
            set(thread_properties.keys()),
            set(
                [
                    "reveal_time",
                    "web_page",
                    "intercept_exercise",
                    "release_codes",
                    "date_received",
                ]
            ),
        )
        self.assertEqual("Test Page URL", thread_properties["web_page"]["url"])
        self.assertEqual(
            "Test Release Code", thread_properties["release_codes"][0]["release_code"]
        )


class EmailAPITestCase(PhishtrayAPIBaseTest):
    def test_email_list_block_public(self):
        """
        Non admin users should not be able to retrieve the email list.
        """
        url = reverse("api:email-list")
        response = self.client.get(url)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_email_list_allow_admin(self):
        """
        Admin users should be able to retrieve the email list.
        """
        url = reverse("api:email-list")
        email_count = 3
        EmailFactory.create_batch(email_count)

        response = self.admin_client.get(url)
        serialized = ExerciseEmailSerializer(ExerciseEmail.objects.all(), many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(email_count, len(response.data))
        self.assertEqual(serialized.data, underscoreize(response.data))

    def test_get_email_details(self):
        """
        Email details are public.
        """
        email_1 = EmailFactory()
        url = reverse("api:email-detail", args=[email_1.id])

        response = self.client.get(url)

        serialized = ExerciseEmailSerializer(ExerciseEmail.objects.get(pk=email_1.id))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, serialized.data)

    def test_get_email_details_404(self):
        """
        Email details are public.
        """
        fake_id = "fakeID"
        url = reverse("api:email-detail", args=[fake_id])

        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual("Not found.", response.data.get("detail"))


class ThreadAPITestCase(PhishtrayAPIBaseTest, ThreadTestsMixin):
    def test_thread_list_block_public(self):
        """
        Non admin users should not be able to retrieve thread list.
        """
        url = reverse("api:thread-list")
        response = self.client.get(url)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_thread_list_allow_admin(self):
        """
        Admin users should be able to retrieve thread list.
        """
        url = reverse("api:thread-list")
        email_count = randint(3, 5)
        emails = EmailFactory.create_batch(email_count)

        self.threadify(emails[0])
        self.threadify(emails[1])

        email_1 = emails[2]
        email_1.replies.add(EmailReplyFactory())
        email_1.attachments.add(ExerciseFileFactory())
        email_1.belongs_to = emails[0]
        email_1.save()

        response = self.admin_client.get(url)
        serialized = ThreadSerializer(
            ExerciseEmail.objects.filter(pk=F("belongs_to")), many=True
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # There should be only 2 threads
        self.assertEqual(2, len(response.data))
        self.assertEqual(serialized.data, underscoreize(response.data))

    def test_get_thread_details(self):
        """
        Thread details are public.
        """

        email_1 = EmailFactory()
        email_1.replies.add(EmailReplyFactory())
        email_1.replies.add(EmailReplyFactory())
        email_1.attachments.add(ExerciseFileFactory())
        # This is how the email becomes a thread (for now...)
        email_1.belongs_to = email_1
        email_1.save()

        # add some emails to email_1 to make it a thread
        email_count = randint(1, 3)
        emails = EmailFactory.create_batch(email_count)

        for email in emails:
            email.belongs_to = email_1
            email.save()

        url = reverse("api:thread-detail", args=[email_1.id])

        response = self.client.get(url)
        serialized = ThreadSerializer(ExerciseEmail.objects.get(pk=email_1.id))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serialized.data, underscoreize(response.data))
        #  +1 because itself will be listed in emails too
        self.assertEqual(email_count + 1, len(response.data.get("emails")))
        self.assertEqual(2, len(response.data.get("replies")))
        self.assertEqual(1, len(response.data.get("attachments")))

    def test_get_thread_details_404(self):
        fake_id = "fakeID"
        url = reverse("api:thread-detail", args=[fake_id])

        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class ExerciseReportsTestCase(PhishtrayAPIBaseTest):
    def test_exercise_reports_list_block_public(self):
        """
        Non admin users should not be able to retrieve exercise reports.
        """
        url = reverse("api:exercise-report-list")
        response = self.client.get(url)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_exercise_reports_list_allow_admin(self):
        """
        Non admin users should not be able to retrieve exercise reports.
        """
        ExerciseFactory.create_batch(2)

        url = reverse("api:exercise-report-list")
        response = self.admin_client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.data))

    def test_exercise_report_details_block_public(self):
        """
        Non admin users should not be able to retrieve exercise reports.
        """
        url = reverse("api:exercise-report-detail", args=["some-uuid-1234"])
        response = self.client.get(url)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_exercise_report_details_allow_admin(self):
        """
        An exercise report should list the exercise ID, title
        and the participants who took the exercise.
        Each participant object contains its demographic profile and a url to download
        their action as CSV.
        """
        # Set up an exercise with some demographic questions
        question_1 = DemographicsInfoFactory()
        question_2 = DemographicsInfoFactory()
        exercise = ExerciseFactory()
        exercise.demographics.add(*[question_1, question_2])
        exercise.save()

        # Participant 1
        entry_1_1 = ProfileEntryFactory(demographics_info=question_1)
        entry_1_2 = ProfileEntryFactory(demographics_info=question_2)
        participant_1 = ParticipantFactory(exercise=exercise)
        participant_1.profile.add(*[entry_1_1, entry_1_2])
        participant_1.save()

        # Participant 2
        entry_2_1 = ProfileEntryFactory(demographics_info=question_1)
        entry_2_2 = ProfileEntryFactory(demographics_info=question_2)
        participant_2 = ParticipantFactory(exercise=exercise)
        participant_2.profile.add(*[entry_2_1, entry_2_2])
        participant_2.save()

        url = reverse("api:exercise-report-detail", args=[exercise.id.hex])
        response = self.admin_client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(str(exercise.id), response.data["id"])
        self.assertEqual(exercise.title, response.data["title"])
        self.assertEqual(2, len(response.data["participants"]))

        # Check that participants have the correct answer
        def get_participant_by_id(participant_id):
            participants = response.data["participants"]
            for p in participants:
                if p["id"] == str(participant_id):
                    return p
            return None

        # Participant 1
        expected_profile_entries_1 = [str(e.id) for e in participant_1.profile.all()]
        response_participant_1 = get_participant_by_id(participant_1.id)
        response_profile_entries_1 = [
            e["id"] for e in response_participant_1["profile"]
        ]
        self.assertSetEqual(
            {*expected_profile_entries_1}, {*response_profile_entries_1}
        )

        # Participant 2
        expected_profile_entries_2 = [str(e.id) for e in participant_2.profile.all()]
        response_participant_2 = get_participant_by_id(participant_2.id)
        response_profile_entries_2 = [
            e["id"] for e in response_participant_2["profile"]
        ]
        self.assertSetEqual(
            {*expected_profile_entries_2}, {*response_profile_entries_2}
        )
