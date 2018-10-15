from django.test import TestCase

from ..factories import (
    EmailFactory,
    ExerciseFactory
)

from ..models import ExerciseEmailProperties


class ExerciseModelTests(TestCase):

    def test_set_email_reveal_times_with_no_emails(self):
        exercise = ExerciseFactory()

        self.assertEqual(0, exercise.emails.all().count())
        exercise_reveal_times = ExerciseEmailProperties.objects.filter(exercise=exercise)
        self.assertEqual(0, exercise_reveal_times.count())

    def test_set_email_reveal_times_with_less_than_ten_emails(self):
        emails = EmailFactory.create_batch(4)
        exercise = ExerciseFactory.create(emails=emails)
        exercise_reveal_times = ExerciseEmailProperties.objects.filter(exercise=exercise)

        exercise.set_email_reveal_times()
        received_emails = [e for e in exercise_reveal_times if e.reveal_time is 0]

        self.assertEqual(4, exercise.emails.all().count())
        self.assertEqual(1, len(received_emails))

    def test_set_email_reveal_times_with_more_than_ten_emails(self):
        emails = EmailFactory.create_batch(27)
        exercise = ExerciseFactory.create(emails=emails)
        exercise_reveal_times = ExerciseEmailProperties.objects.filter(exercise=exercise)

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
        exercise_reveal_times = ExerciseEmailProperties.objects.filter(exercise=exercise)

        exercise.set_email_reveal_times()
        received_emails = [e for e in exercise_reveal_times if e.reveal_time is 0]
        received_email_ids = [re.id for re in exercise.emails.all()]

        self.assertEqual(35, exercise.emails.all().count())
        self.assertTrue(3 <= len(received_emails) <= 5)

        exercise.title = 'Updated Exercise'
        exercise.save()

        received_email_ids_after_update = [re.id for re in exercise.emails.all()]
        self.assertEqual(set(received_email_ids), set(received_email_ids_after_update))
