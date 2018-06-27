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
        self.assertEmail1(json_data)

    def test_emails_list(self):
        self.create_emails()

        response = self.client.get('/exercise/emails/list/')
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        self.assertEmail1(json_data[0])

        self.assertEqual(json_data[1]['id'], 2)
        self.assertEqual(json_data[1]['subject'], 'test email from unit test case-2')
        self.assertEqual(json_data[1]['from_address'], 'test2@cybsafe.com')
        self.assertEqual(json_data[1]['from_name'], 'Cybsafe Admin-2')
        self.assertEqual(json_data[1]['to_address'], 'sendTo2@cybsafe.com')
        self.assertEqual(json_data[1]['to_name'], 'Cybsafe Admin-2')
        self.assertEqual(json_data[1]['phish_type'], 1)
        self.assertEqual(json_data[1]['replies'][0]['id'], 1)
        self.assertEqual(json_data[1]['replies'][0]['reply_type'], 1)
        self.assertEqual(json_data[1]['replies'][0]['message'], 'I have received your email-1')
        self.assertEqual(json_data[1]['attachments'][0]['id'], 1)
        self.assertEqual(json_data[1]['attachments'][0]['filename'], 'location of file name')

    def assertEmail1(self, json_data):
        self.assertEqual(json_data['id'], 1)
        self.assertEqual(json_data['subject'], 'test email from unit test case')
        self.assertEqual(json_data['from_address'], 'test@cybsafe.com')
        self.assertEqual(json_data['from_name'], 'Cybsafe Admin')
        self.assertEqual(json_data['to_address'], 'sendTo1@cybsafe.com')
        self.assertEqual(json_data['to_name'], 'Cybsafe Admin-1')
        self.assertEqual(json_data['phish_type'], 0)
        self.assertEqual(json_data['replies'][0]['id'], 1)
        self.assertEqual(json_data['replies'][0]['reply_type'], 1)
        self.assertEqual(json_data['replies'][0]['message'], 'I have received your email-1')
        self.assertEqual(json_data['attachments'][0]['id'], 1)
        self.assertEqual(json_data['attachments'][0]['filename'], 'location of file name')

    @staticmethod
    def create_emails():
        replies = ExerciseEmailReply(
            id=1,
            reply_type=1,
            message='I have received your email-1'

        )
        replies.save()
        attachment = ExerciseAttachment(
            id = 1,
            filename ='location of file name'
        )
        attachment.save()
        email1 = ExerciseEmail(
            id=1,
            subject='test email from unit test case',
            from_address='test@cybsafe.com',
            from_name='Cybsafe Admin',
            to_address='sendTo1@cybsafe.com',
            to_name='Cybsafe Admin-1',
            phish_type=0,
            content="Hello world",
        )
        email1.save()
        email1.replies.add(replies)
        email1.attachments.add(attachment)
        email2 = ExerciseEmail(
            id=2,
            subject='test email from unit test case-2',
            from_address='test2@cybsafe.com',
            from_name='Cybsafe Admin-2',
            to_address='sendTo2@cybsafe.com',
            to_name='Cybsafe Admin-2',
            phish_type=1,
            content="Hello world-2")
        email2.save()
        email2.replies.add(replies)
        email2.attachments.add(attachment)