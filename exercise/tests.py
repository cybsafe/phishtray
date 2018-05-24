from django.test import TestCase
from django.urls import reverse

from .models import Exercise


class ExerciseModelTests(TestCase):

    def test_link_capability_in_exercise(self):
        """
        tests the salted hash function to obfuscate experiment ID's
        """
        exercise = Exercise(id=1)
        self.assertEqual(exercise.link, "WLE")


class ExerciseViewTests(TestCase):

    def test_exercise_link_resolve(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        link = "WLE"
        exercise = Exercise(
            id=1,
            length_minutes=10,
        )
        exercise.save()

        response = self.client.get(reverse('exercise:index', args=(link,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "WLE")
