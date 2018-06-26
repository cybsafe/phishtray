from django.test import TestCase
from django.urls import reverse

from .models import *

import json

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


class ExerciseRestTests(TestCase):

    def test_exercise_not_found(self):
        response = self.client.get('/exercise/list/1/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual((json.loads(response.content))['detail'], 'Not found.')

    def test_exercise_by_id(self):
        self.create_exercise()

        response = self.client.get('/exercise/list/1/')
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        self.assertEqual(json_data['id'], 1)
        self.assertEqual(json_data['title'], 'first exercise')
        self.assertEqual(json_data['description'], 'test desc')
        self.assertEqual(json_data['length_minutes'], 10)
        self.assertIsNotNone(json_data['created_date'])
        self.assertIsNotNone(json_data['modified_date'])

    def create_exercise(self):
        exercise = Exercise(
            id=1,
            title='first exercise',
            description='test desc',
            length_minutes=10
        )
        exercise.save()


class ExerciseEmailTests(TestCase):

    def test_exercise_emails_not_found(self):
        response = self.client.get('/exercise/emails/1/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual((json.loads(response.content))['detail'], 'Not found.')

    def test_emails_by_id(self):
        self.create_emails()

        response = self.client.get('/exercise/emails/1/')
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        self.assertEqual(json_data['id'], 1)
        self.assertEqual(json_data['title'], 'first exercise')
        self.assertEqual(json_data['description'], 'test desc')
        self.assertEqual(json_data['length_minutes'], 10)
        self.assertIsNotNone(json_data['created_date'])
        self.assertIsNotNone(json_data['modified_date'])

    def create_emails(self):
        email1 = ExerciseEmail(
            id=1,
            subject='test email from unit test case',
            email_from_email='test@cybsafe.com',
            email_from_name ='Cybsafe Admin',
            type = 0,
            content = "Hello world")
        email1.save()