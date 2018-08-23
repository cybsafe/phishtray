import json
from django.test import TestCase
from django.urls import reverse

from exercise.models import *
from .helpers.assert_emal_response import EmailAssertHelper
from ..factories import (
    EmailFactory,
    ExerciseFactory
)


class ExerciseModelTests(TestCase):

    def test_link_capability_in_exercise(self):
        """
        tests the salted hash function to obfuscate experiment ID's
        """
        exercise = ExerciseFactory()
        self.assertEqual(exercise.link, "WLE")

    def test_set_email_reveal_times_with_no_emails(self):
        exercise = ExerciseFactory()

        self.assertEqual(0, exercise.emails.all().count())
        self.assertIsNone(exercise.email_reveal_times)

    def test_set_email_reveal_times_with_less_then_ten_emails(self):
        emails = EmailFactory.create_batch(4)
        exercise = ExerciseFactory.create(emails=emails)

        received_emails = [e for e in exercise.email_reveal_times if e['reveal_time'] is 0]

        self.assertEqual(4, exercise.emails.all().count())
        self.assertEqual(0, len(received_emails))

    def test_set_email_reveal_times_with_more_then_ten_emails(self):
        emails = EmailFactory.create_batch(27)
        exercise = ExerciseFactory.create(emails=emails)

        received_emails = [e for e in exercise.email_reveal_times if e['reveal_time'] is 0]

        self.assertEqual(27, exercise.emails.all().count())
        self.assertEqual(2, len(received_emails))

    def test_sticky_received_emails(self):
        """
        Current logic dictates that received emails shouldn't change after saving the Exercise.
        """
        emails = EmailFactory.create_batch(35)
        exercise = ExerciseFactory.create(emails=emails)

        received_emails = [e for e in exercise.email_reveal_times if e['reveal_time'] is 0]
        received_email_ids = [re['email_id'] for re in received_emails]
        self.assertEqual(35, exercise.emails.all().count())
        self.assertEqual(3, len(received_emails))

        exercise.title = 'Updated Exercise'
        exercise.save()

        received_emails_after_update = [e for e in exercise.email_reveal_times if e['reveal_time'] is 0]
        received_email_ids_after_update = [re['email_id'] for re in received_emails_after_update]
        self.assertEqual(set(received_email_ids), set(received_email_ids_after_update))


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
        EmailAssertHelper.assert_first_email(self,json_data['emails'][0])

    @staticmethod
    def create_exercise():
        exercise = Exercise(
            id=1,
            title='first exercise',
            description='test desc',
            length_minutes=10
        )
        exercise.save()
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
        exercise.emails.add(email1)


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
        EmailAssertHelper.assert_first_email(self, json_data)

    def test_emails_list(self):
        self.create_emails()

        response = self.client.get('/exercise/emails/list/')
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        EmailAssertHelper.assert_first_email(self, json_data[0])
        EmailAssertHelper.assert_second_email(self, json_data[1])


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