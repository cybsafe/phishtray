from django.test import TestCase

from ..factories import (
    EmailFactory,
    ExerciseFactory
)


class ExerciseModelTests(TestCase):

    def test_set_email_reveal_times_with_no_emails(self):
        exercise = ExerciseFactory()

        self.assertEqual(0, exercise.emails.all().count())
        self.assertIsNone(exercise.email_reveal_times)

    def test_set_email_reveal_times_with_less_then_ten_emails(self):
        emails = EmailFactory.create_batch(4)
        exercise = ExerciseFactory.create(emails=emails)

        received_emails = [e for e in exercise.email_reveal_times if e['reveal_time'] is 0]

        self.assertEqual(4, exercise.emails.all().count())
        self.assertEqual(0, len(received_emails))

    def test_set_email_reveal_times_with_more_then_ten_emails(self):
        emails = EmailFactory.create_batch(27)
        exercise = ExerciseFactory.create(emails=emails)

        received_emails = [e for e in exercise.email_reveal_times if e['reveal_time'] is 0]

        self.assertEqual(27, exercise.emails.all().count())
        self.assertEqual(2, len(received_emails))

    def test_sticky_received_emails(self):
        """
        Current logic dictates that received emails shouldn't change after saving the Exercise.
        """
        emails = EmailFactory.create_batch(35)
        exercise = ExerciseFactory.create(emails=emails)

        received_emails = [e for e in exercise.email_reveal_times if e['reveal_time'] is 0]
        received_email_ids = [re['email_id'] for re in received_emails]
        self.assertEqual(35, exercise.emails.all().count())
        self.assertEqual(3, len(received_emails))

        exercise.title = 'Updated Exercise'
        exercise.save()

        received_emails_after_update = [e for e in exercise.email_reveal_times if e['reveal_time'] is 0]
        received_email_ids_after_update = [re['email_id'] for re in received_emails_after_update]
        self.assertEqual(set(received_email_ids), set(received_email_ids_after_update))
