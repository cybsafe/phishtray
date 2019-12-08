from django.test import TestCase
from django.db import IntegrityError

from ..factories import (
    EmailFactory,
    ExerciseFactory,
    EmailReplyFactory,
    EmailReplyTaskScoreFactory,
    ExerciseTaskFactory,
    ExerciseWebPageFactory,
    ExerciseWebPageReleaseCodeFactory,
)
from ..models import ExerciseEmailProperties, ExerciseWebPage, Exercise
from exercise.serializer import (
    ExerciseWebPageSerializer,
    ExerciseEmailPropertiesSerializer,
)
from participant.factories import OrganizationFactory
from django.utils import timezone


class ExerciseModelTests(TestCase):
    def test_set_email_reveal_times_with_no_emails(self):
        exercise = ExerciseFactory()

        self.assertEqual(0, exercise.emails.all().count())
        exercise_reveal_times = ExerciseEmailProperties.objects.filter(
            exercise=exercise
        )
        self.assertEqual(0, exercise_reveal_times.count())

    def test_set_email_reveal_times_with_less_than_ten_emails(self):
        emails = EmailFactory.create_batch(4)
        exercise = ExerciseFactory.create(emails=emails)

        exercise.set_email_reveal_times()
        received_emails = [
            e for e in exercise.emails.all() if e.reveal_time(exercise) is 0
        ]

        self.assertEqual(4, exercise.emails.all().count())
        self.assertEqual(1, len(received_emails))

    def test_set_email_reveal_times_with_more_than_ten_emails(self):
        emails = EmailFactory.create_batch(27)
        exercise = ExerciseFactory.create(emails=emails)
        exercise_reveal_times = ExerciseEmailProperties.objects.filter(
            exercise=exercise
        )

        exercise.set_email_reveal_times()
        received_emails = [e for e in exercise_reveal_times if e.reveal_time is 0]

        self.assertEqual(27, exercise.emails.all().count())
        self.assertTrue(2 <= len(received_emails) <= 4)

    def test_sticky_received_emails(self):
        """
        Current logic dictates that received emails shouldn't change after saving the Exercise.
        """
        emails = EmailFactory.create_batch(35)
        exercise = ExerciseFactory.create(emails=emails)
        exercise_reveal_times = ExerciseEmailProperties.objects.filter(
            exercise=exercise
        )

        exercise.set_email_reveal_times()
        received_emails = [e for e in exercise_reveal_times if e.reveal_time is 0]
        received_email_ids = [re.id for re in exercise.emails.all()]

        self.assertEqual(35, exercise.emails.all().count())
        self.assertTrue(3 <= len(received_emails) <= 5)

        exercise.title = "Updated Exercise"
        exercise.save()

        received_email_ids_after_update = [re.id for re in exercise.emails.all()]
        self.assertEqual(set(received_email_ids), set(received_email_ids_after_update))

    def test_email_reply_scoring(self):
        """
        Test the EmailReply.score()
        """
        task = ExerciseTaskFactory(
            name="Legend Score",
            debrief_over_threshold="Well done for being a legend",
            debrief_under_threshold="Try harder to reach legend status",
            score_threshold=3,
        )

        email_reply = EmailReplyFactory()

        score_one = EmailReplyTaskScoreFactory(
            task=task, value=4, email_reply=email_reply
        )

        score_two = EmailReplyTaskScoreFactory(task=task, value=2)

        self.assertTrue(score_one in email_reply.scores)
        self.assertFalse(score_two in email_reply.scores)

    def test_exercise_specific_properties(self):
        emails = EmailFactory.create_batch(1)
        exercise = ExerciseFactory.create(emails=emails)
        email_properties = ExerciseEmailProperties.objects.filter(
            exercise=exercise
        ).first()

        email_properties.web_page = ExerciseWebPageFactory(url="Page URL 1")
        email_properties.release_codes.add(
            ExerciseWebPageReleaseCodeFactory(release_code="Release Code 1")
        )
        email_properties.save()

        exercise_specific_properties = email_properties.email.exercise_specific_properties(
            exercise
        )

        self.assertEqual("Page URL 1", exercise_specific_properties.web_page.url)
        self.assertEqual(
            "Release Code 1",
            exercise_specific_properties.release_codes.first().release_code,
        )
        self.assertFalse(exercise_specific_properties.intercept_exercise)

    def test_when_no_exercise_specific_properties(self):
        emails = EmailFactory.create_batch(1)
        exercise = ExerciseFactory.create(emails=emails)
        email_properties = ExerciseEmailProperties.objects.filter(
            exercise=exercise, email=emails[0]
        )

        other_email = EmailFactory()
        properties_with_invalid_email = ExerciseEmailProperties.objects.filter(
            exercise=exercise, email=other_email
        )

        self.assertEqual(1, email_properties.count())
        self.assertEqual(0, properties_with_invalid_email.count())

    def test_create_public_exercise(self):
        emails = EmailFactory.create_batch(2)
        exercise = ExerciseFactory.create(emails=emails)

        self.assertIsNotNone(exercise)
        self.assertIsNone(exercise.organization)

    def test_create_private_exercise(self):
        emails = EmailFactory.create_batch(2)
        org = OrganizationFactory()
        exercise = ExerciseFactory.create(emails=emails, organization=org)
        exercise2 = ExerciseFactory()

        self.assertIsNotNone(exercise)
        self.assertIsNotNone(exercise.organization)
        self.assertEqual(2, Exercise.objects.all().count())
        self.assertEqual(1, Exercise.objects.filter(organization=org).count())

    def test_copied_from_exercise_id(self):
        base_exercise = ExerciseFactory()
        copied_from_str = f"{base_exercise.title} - {base_exercise.id}"

        test_params = [
            {"exercise": base_exercise, "expected_result": None},
            {"exercise": ExerciseFactory(copied_from=None), "expected_result": None},
            {
                "exercise": ExerciseFactory(copied_from="some random string"),
                "expected_result": None,
            },
            {
                "exercise": ExerciseFactory(copied_from=copied_from_str),
                "expected_result": str(base_exercise.id),
            },
        ]

        for params in test_params:
            with self.subTest(params=params):
                self.assertEquals(
                    params["expected_result"],
                    params["exercise"].copied_from_exercise_id,
                )

    def test_copied_from_exercise(self):
        base_exercise = ExerciseFactory()
        copied_from_str = f"{base_exercise.title} - {base_exercise.id}"

        test_params = [
            {"exercise": base_exercise, "expected_result": None},
            {"exercise": ExerciseFactory(copied_from=None), "expected_result": None},
            {
                "exercise": ExerciseFactory(copied_from="some random string"),
                "expected_result": None,
            },
            {
                "exercise": ExerciseFactory(copied_from=copied_from_str),
                "expected_result": base_exercise,
            },
        ]

        for params in test_params:
            with self.subTest(params=params):
                self.assertEquals(
                    params["expected_result"], params["exercise"].copied_from_exercise
                )


class ExerciseWebPageModelTests(TestCase):
    def test_url_uniqueness(self):
        org = OrganizationFactory()
        ExerciseWebPage.objects.create(
            url="https://www.emtray.com/welcome", organization=org
        )

        with self.assertRaises(IntegrityError):
            ExerciseWebPage.objects.create(
                url="https://www.emtray.com/welcome", organization=org
            )

    def test_default_page_type(self):
        page = ExerciseWebPage.objects.create(url="https://www.emtray.com/welcome")
        self.assertEqual(ExerciseWebPage.PAGE_REGULAR, page.type)


class ExerciseWebPageSerializerTests(TestCase):
    def test_expected_fields(self):
        web_page = ExerciseWebPage.objects.create()
        data = ExerciseWebPageSerializer(instance=web_page).data

        self.assertEqual(set(data.keys()), set(["title", "url", "type", "content"]))


class ExerciseEmailPropertiesSerializerTests(TestCase):
    def test_expected_fields_and_contents(self):
        emails = EmailFactory.create_batch(1)
        exercise = ExerciseFactory.create(emails=emails)
        email_properties = ExerciseEmailProperties.objects.filter(
            exercise=exercise
        ).first()
        email_properties.web_page = ExerciseWebPageFactory(url="Page URL 1")
        release_code = ExerciseWebPageReleaseCodeFactory(release_code="Release Code 1")
        email_properties.release_codes.add(release_code)
        data = ExerciseEmailPropertiesSerializer(instance=email_properties).data
        self.assertEqual(
            set(data.keys()),
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
        self.assertEqual("Page URL 1", data["web_page"]["url"])
        self.assertEqual(
            set(data["web_page"].keys()), set(["title", "url", "type", "content"])
        )
        self.assertEqual("Release Code 1", data["release_codes"][0]["release_code"])


class ExerciseReceivedDateTests(TestCase):
    """
    Tests that reveal_time becomes, and remains, 0
    if or when date_received is set.
    """

    def setUp(self):
        self.time = timezone.now()
        emails = EmailFactory.create_batch(1)
        exercise = ExerciseFactory.create(emails=emails)
        self.email_properties = ExerciseEmailProperties.objects.filter(
            exercise=exercise
        ).first()

    def test_when_date_received_is_set_and_reveal_time_is_none(self):
        self.email_properties.reveal_time = None
        self.email_properties.save()
        self.assertEqual(None, self.email_properties.reveal_time)

        self.email_properties.date_received = self.time
        self.email_properties.save()
        self.assertEqual(0, self.email_properties.reveal_time)

    def test_when_date_received_is_set_and_reveal_time_has_value(self):
        self.email_properties.reveal_time = 44
        self.email_properties.save()
        self.assertEqual(44, self.email_properties.reveal_time)

        self.email_properties.date_received = self.time
        self.email_properties.save()
        self.assertEqual(0, self.email_properties.reveal_time)

    def test_if_date_received_is_set_no_reveal_time_change(self):
        self.email_properties.reveal_time = 10
        self.email_properties.date_received = self.time
        self.email_properties.save()

        self.assertEqual(0, self.email_properties.reveal_time)

    def test_if_date_received_not_set_reveal_time_may_be_changed(self):
        self.email_properties.reveal_time = 44
        self.email_properties.save()

        self.assertEqual(44, self.email_properties.reveal_time)
