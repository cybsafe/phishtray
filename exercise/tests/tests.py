from django.test import TestCase
from django.urls import reverse

from exercise.models import *
from exercise.tests.helpers.assert_emal_response import *
from participant.models import Participant

import json

class ExerciseModelTests(TestCase):

    def test_link_capability_in_exercise(self):
        """
        tests the salted hash function to obfuscate experiment ID's
        """
        exercise = Exercise(id=1)
        self.assertEqual(exercise.link, "WLE")

    def test_contextualized_emails_immediately_available_amount(self):
        """
        tests that the 10% of the emails have the reveal time set to 0
        """
        emails = [ExerciseEmail.objects.create(phish_type=EXERCISE_EMAIL_PHISH) for _ in range(10)]
        exercise = Exercise.objects.create(length_minutes=10)

        exercise.emails.add(*emails)

        contextualized_emails = list(exercise.contextualized_emails)
        immediately_available_emails = [email for email in contextualized_emails if email.reveal_time == 0]

        # 10% of the emails should be immediately available
        self.assertEqual(len(contextualized_emails), 10)
        self.assertEqual(len(immediately_available_emails), 1)

    def test_contextualized_emails_reveal_time_consistency(self):
        """
        tests that the reveal time is consistent for the same email in the same exercise for every participant
        """
        emails = [ExerciseEmail.objects.create(phish_type=EXERCISE_EMAIL_PHISH) for _ in range(10)]
        exercise1 = Exercise.objects.create(length_minutes=10)
        exercise2 = Exercise.objects.create(length_minutes=15)
        participant1 = Participant.objects.create(exercise=exercise1)
        participant2 = Participant.objects.create(exercise=exercise1)

        exercise1.emails.add(*emails)
        exercise2.emails.add(*emails)

        # The same email has a different reveal time for different exercises
        email1_exercise1 = next(exercise1.contextualized_emails)
        email1_exercise2 = next(exercise2.contextualized_emails)
        self.assertEquals(email1_exercise1, email1_exercise2)
        self.assertNotEqual(email1_exercise1.reveal_time, email1_exercise2.reveal_time)

        # The same email has the same reveal time for the same exercise for every participant
        self.assertEqual(participant1.exercise, participant2.exercise)
        participant1_emails = sorted(participant1.exercise.contextualized_emails, key=lambda e: e.id)
        participant2_emails = sorted(participant2.exercise.contextualized_emails, key=lambda e: e.id)
        for email1, email2 in zip(participant1_emails, participant2_emails):
            self.assertEqual(email1, email2)
            self.assertEqual(email1.reveal_time, email2.reveal_time)


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