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

        # To see what's going on
        print(f"\n Exercise 1: {exercise_1.id}")
        print(f"Copied Exercise: {copied_exercise.id}")
        print(
            f"Copied from exercise (Should be exercise1's id'): {copied_exercise.copied_from.id}"
        )

        self.assertIsNotNone(copied_exercise)
        self.assertEqual(str(exercise_1.id), str(copied_exercise.copied_from.id))
        self.assertEqual(3, Exercise.objects.all().count())
        self.assertEqual(1, Exercise.objects.filter(copied_from=exercise_1).count())
