from django.test import TestCase

from exercise.factories import ExerciseFactory
from exercise.models import Exercise


class PhishtrayBaseModelTest(TestCase):
    def setUp(self):
        self.exercise_1 = ExerciseFactory()
        self.exercise_2 = ExerciseFactory()

    def test_soft_delete(self):
        # IMPORTANT soft delete is being deprecated, at this point it should work as delete

        # Check that we have all Exercises
        self.assertEqual(2, Exercise.objects.count())

        self.exercise_1.delete()
        self.assertFalse(Exercise.objects.filter(pk=self.exercise_1.id))
        self.assertEqual(1, Exercise.objects.count())

        # The record should be deleted from the DB as well
        raw_exercises = Exercise.objects.raw("SELECT * FROM exercise_exercise")

        all_exercises = [e for e in raw_exercises]
        deleted_exercises = [e for e in raw_exercises if e.deleted_at]
        undeleted_exercises = [e for e in raw_exercises if not e.deleted_at]

        self.assertEqual(1, len(all_exercises))
        self.assertEqual(0, len(deleted_exercises))
        self.assertEqual(1, len(undeleted_exercises))

    def test_hard_delete(self):
        self.exercise_1.hard_delete()
        self.assertFalse(Exercise.objects.filter(pk=self.exercise_1.id))
        self.assertEqual(1, Exercise.objects.all().count())

        # Get all records from the DB
        raw_exercises = Exercise.objects.raw("SELECT * FROM exercise_exercise")
        all_exercises = [e for e in raw_exercises]
        deleted_exercises = [e for e in raw_exercises if e.deleted_at]
        undeleted_exercises = [e for e in raw_exercises if not e.deleted_at]

        self.assertEqual(1, len(all_exercises))
        self.assertEqual(0, len(deleted_exercises))
        self.assertEqual(1, len(undeleted_exercises))
