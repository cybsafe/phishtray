from django.test import TestCase
from ..factories import ExerciseFactory
from ..models import Exercise
from ..helpers import copy_exercise


class ExerciseHelperTests(TestCase):
    def test_copy_exercise(self):
        """
        Testing helper method that copies an exercise
        """
        exercise_1 = ExerciseFactory()
        copied_exercise = copy_exercise(exercise_1)

        self.assertIsNotNone(copied_exercise)
        self.assertEqual(2, Exercise.objects.all().count())

        self.assertEqual(str(exercise_1.id), str(copied_exercise.copied_from.id))
        self.assertEqual(
            exercise_1.demographics.all().count(),
            copied_exercise.demographics.all().count(),
        )
        self.assertEqual(
            exercise_1.emails.all().count(), copied_exercise.emails.all().count()
        )
        self.assertEqual(
            exercise_1.files.all().count(), copied_exercise.files.all().count()
        )

        self.assertEqual(1, Exercise.objects.filter(copied_from=exercise_1).count())
