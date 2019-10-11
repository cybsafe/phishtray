from django.test import TestCase
from ..factories import ExerciseFactory
from ..models import Exercise
from ..helpers import copy_exercise


class ExerciseHelperTests(TestCase):
    def setUp(self):
        self.exercise_1 = ExerciseFactory()
        self.exercise_2 = ExerciseFactory()

    def test_copy_exercise(self):
        """
        Testing helper method that copies an exercise
        """

        copied_exercise = copy_exercise(self.exercise_1)
        self.assertIsNotNone(copied_exercise)

        print(f"Exercise 1: {self.exercise_1.id}")
        print(f"Copied Exercise: {copied_exercise.id}")
        print(
            f"Copied from exercise (Should be exercise1): {copied_exercise.copied_from.id}"
        )
        # print(f"Exercise 1: {self.exercise_1.id}")

        self.assertEqual(copied_exercise.copied_from, self.exercise_1)
        self.assertEqual(3, Exercise.objects.all().count())
        self.assertEqual(
            1, Exercise.objects.filter(copied_from=self.exercise_1).count()
        )
