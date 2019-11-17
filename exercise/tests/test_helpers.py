from django.test import TestCase
from ..factories import ExerciseFactory
from ..models import Exercise
from ..helpers import copy_exercise, add_trial

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
        self.assertEqual(exercise, copied_exercise.copied_from_exercise)
        self.assertEqual(1, copied_exercise.trial_version)
        self.assertIsNone(copied_exercise.initial_trial)
        self.assertEqual(2, Exercise.objects.all().count())

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

    def test_trial_exercise(self):
        """
        Testing helper method that make a trial of an exercise
        """
        self.organization = OrganizationFactory()
        self.user = UserFactory(
            username="user_with_organization", organization=self.organization
        )
        exercise = ExerciseFactory(organization=self.organization)
        trial_exercise = add_trial(exercise, self.user)

        self.assertIsNotNone(trial_exercise)
        self.assertEqual(2, Exercise.objects.all().count())

        self.assertEqual(exercise, trial_exercise.copied_from_exercise)
        self.assertEqual(exercise, trial_exercise.initial_trial)

        self.assertEqual(2, trial_exercise.trial_version)

        self.assertEqual(
            exercise.demographics.all().count(),
            trial_exercise.demographics.all().count(),
        )
        self.assertEqual(
            exercise.emails.all().count(), trial_exercise.emails.all().count()
        )
        self.assertEqual(
            exercise.files.all().count(), trial_exercise.files.all().count()
        )

        self.assertEqual(1, Exercise.objects.filter(copied_from=exercise).count())

    def test_trial_exercises(self):
        """
        Testing helper method that make trials of an exercise
        """
        self.organization = OrganizationFactory()
        self.user = UserFactory(
            username="user_with_organization", organization=self.organization
        )
        exercise = ExerciseFactory(organization=self.organization)
        trial_exercise = add_trial(exercise, self.user)
        another_trial_exercise = add_trial(exercise, self.user)

        self.assertIsNotNone(trial_exercise)
        self.assertIsNotNone(another_trial_exercise)
        self.assertEqual(3, Exercise.objects.all().count())

        self.assertEqual(exercise, trial_exercise.copied_from_exercise)
        self.assertEqual(exercise, another_trial_exercise.copied_from_exercise)

        self.assertEqual(exercise, trial_exercise.initial_trial)
        self.assertEqual(exercise, another_trial_exercise.initial_trial)

        self.assertEqual(2, trial_exercise.trial_version)
        self.assertEqual(3, another_trial_exercise.trial_version)

        self.assertEqual(2, Exercise.objects.filter(copied_from=exercise).count())
        self.assertEqual(2, Exercise.objects.filter(initial_trial=exercise).count())
