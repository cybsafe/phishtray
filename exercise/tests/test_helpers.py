from django.test import TestCase
from ..factories import ExerciseFactory
from ..models import Exercise
from ..helpers import copy_exercise

from participant.factories import OrganizationFactory
from users.factories import UserFactory


class ExerciseHelperTests(TestCase):
    def test_copy_exercise(self):
        """
        Testing helper method that copies an exercise
        """
        exercise = ExerciseFactory()
        self.organization = OrganizationFactory()
        self.user = UserFactory(
            username="user_with_organization", organization=self.organization
        )

        copied_exercise = copy_exercise(exercise, self.user)

        self.assertIsNotNone(copied_exercise)
        self.assertEqual(2, Exercise.objects.all().count())

        self.assertEqual(str(exercise.id), str(copied_exercise.copied_from.id))
        self.assertEqual(
            exercise.demographics.all().count(),
            copied_exercise.demographics.all().count(),
        )
        self.assertEqual(
            exercise.emails.all().count(), copied_exercise.emails.all().count()
        )
        self.assertEqual(
            exercise.files.all().count(), copied_exercise.files.all().count()
        )

        self.assertEqual(1, Exercise.objects.filter(copied_from=exercise).count())
