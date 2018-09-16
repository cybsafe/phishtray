from django.test import TestCase

from exercise.factories import ExerciseFactory
from exercise.models import Exercise


class PhishtrayBaseModelTest(TestCase):

    def setUp(self):
        self.exercise_1 = ExerciseFactory()
        ExerciseFactory.create_batch(10)

    def test_soft_delete(self):
        # Check that we have all Exercises
        self.assertEqual(11, Exercise.objects.all().count())

        # Delete one then we should end up with 10 when accessing the DB with django
        self.exercise_1.delete()
        self.assertFalse(Exercise.objects.filter(pk=self.exercise_1.id))
        self.assertEqual(10, Exercise.objects.all().count())

        # However the record should still be present in the DB
        raw_exercises = Exercise.objects.raw('SELECT * FROM exercise_exercise')

        all_exercises = [e for e in raw_exercises]
        deleted_exercises = [e for e in raw_exercises if e.deleted_at]
        undeleted_exercises = [e for e in raw_exercises if not e.deleted_at]

        self.assertEqual(11, len(all_exercises))
        self.assertEqual(1, len(deleted_exercises))
        self.assertEqual(10, len(undeleted_exercises))

    def test_undo_soft_delete(self):
        # Delete one then we should end up with 10 when accessing the DB with django
        self.exercise_1.delete()
        self.assertFalse(Exercise.objects.filter(pk=self.exercise_1.id))
        self.assertEqual(10, Exercise.objects.all().count())

        exercise = Exercise.all_objects.get(pk=self.exercise_1.id)
        exercise.deleted_at = None
        exercise.save()

        self.assertEqual(11, Exercise.objects.all().count())

    def test_hard_delete(self):
        self.exercise_1.hard_delete()
        self.assertFalse(Exercise.objects.filter(pk=self.exercise_1.id))
        self.assertEqual(10, Exercise.objects.all().count())

        # Get all records from the DB
        raw_exercises = Exercise.objects.raw('SELECT * FROM exercise_exercise')
        all_exercises = [e for e in raw_exercises]
        deleted_exercises = [e for e in raw_exercises if e.deleted_at]
        undeleted_exercises = [e for e in raw_exercises if not e.deleted_at]

        self.assertEqual(10, len(all_exercises))
        self.assertEqual(0, len(deleted_exercises))
        self.assertEqual(10, len(undeleted_exercises))