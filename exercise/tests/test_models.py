from django.test import TestCase

from ..factories import (
    EmailFactory,
    ExerciseFactory,
    EmailReplyFactory,
    EmailReplyTaskScoreFactory,
    ExerciseTaskFactory,
    ExerciseWebPageFactory,
    ExerciseWebPageReleaseCodeFactory,
)

from ..models import (
    ExerciseEmailProperties,
    ExerciseWebPage,
    ExerciseWebPageReleaseCode,
)
from django.db import IntegrityError


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
        exercise_reveal_times = ExerciseEmailProperties.objects.filter(
            exercise=exercise
        )

        exercise.set_email_reveal_times()
        received_emails = [e for e in exercise_reveal_times if e.reveal_time is 0]

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
        emails = EmailFactory.create_batch(5)
        exercise = ExerciseFactory.create(emails=emails)
        email_properties = ExerciseEmailProperties.objects.filter(exercise=exercise)
        self.assertEqual(5, email_properties.count())

        # for cnt, prop in enumerate(email_properties, 1):
        for cnt, prop in enumerate(email_properties, 1):
            prop.web_page = ExerciseWebPageFactory()
            prop.release_codes.add(ExerciseWebPageReleaseCodeFactory())

            prop.intercept_exercise = False if cnt == 4 else True

            prop.save()

            with self.subTest(cnt=cnt):
                test_email_properties = prop.email.exercise_specific_properties
                self.assertEqual(
                    "Page URL {}".format(cnt), test_email_properties.web_page.url
                )
                self.assertEqual(
                    "Release Code {}".format(cnt),
                    test_email_properties.release_codes.first().release_code,
                )

                if cnt == 4:
                    self.assertFalse(test_email_properties.intercept_exercise)
                else:
                    self.assertTrue(test_email_properties.intercept_exercise)

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


class ExerciseWebPageModelTests(TestCase):
    def test_url_uniqueness(self):
        ExerciseWebPage.objects.create(url="https://www.emtray.com/welcome")

        with self.assertRaises(IntegrityError):
            ExerciseWebPage.objects.create(url="https://www.emtray.com/welcome")

    def test_default_page_type(self):
        page = ExerciseWebPage.objects.create(url="https://www.emtray.com/welcome")
        self.assertEqual(ExerciseWebPage.PAGE_REGULAR, page.type)
