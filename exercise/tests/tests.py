from django.test import TestCase
from django.urls import reverse

from exercise.models import *
from exercise.tests.helpers.assert_emal_response import *

import json

from .helpers.prepare_data import create_exercise_3_emails \
                                , create_exercise_20_emails

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
        EmailAssertHelper.assert_first_email(self,json_data['emails'][0])

    #ADefler(raydeal)
    def test_exercise_detail_by_id_1_email_reveal_time_None(self):
        self.create_exercise()

        response = self.client.get('/exercise/detail/1/')
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data['id'], 1)
        self.assertEqual(json_data['title'], 'first exercise')
        self.assertEqual(json_data['description'], 'test desc')
        self.assertEqual(json_data['length_minutes'], 10)
        self.assertIsNotNone(json_data['created_date'])
        self.assertIsNotNone(json_data['modified_date'])
        first_email = json_data['emails'][0]
        EmailAssertHelper.assert_first_email(self,first_email)
        self.assertIn('reveal_time',first_email)
        self.assertIsNone(first_email['reveal_time'])

    def test_exercise_detail_by_id_3_emails_reveal_time_None(self):
        create_exercise_3_emails()

        response = self.client.get('/exercise/detail/1/')
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data['id'], 1)
        self.assertEqual(json_data['title'], 'Exercise A. Changing the world.')
        self.assertEqual(json_data['description'], 'This is the administrator description of the exercise')
        self.assertEqual(json_data['length_minutes'], 5)
        self.assertIsNotNone(json_data['created_date'])
        self.assertIsNotNone(json_data['modified_date'])
        #I don't test emails content because it is nothing new
        #but I test if every emails contain reveal_time set to None
        for email in json_data['emails']:
            self.assertIn('reveal_time',email)
            self.assertIsNone(email['reveal_time'])

    def test_reveal_time_zero_count(self):
        '''tests if reveal_time is zero for 10% of exercise emails'''
        exercise = create_exercise_20_emails()

        response = self.client.get('/exercise/detail/1/')
        self.assertEqual(response.status_code, 200)
        json_data = response.json()

        reveal_time_zero_counter = 0
        for email in json_data['emails']:
            self.assertIn('reveal_time',email)
            reveal_time = int(email['reveal_time'])
            self.assertIsNotNone(reveal_time)
            if 0 == reveal_time:
                reveal_time_zero_counter += 1
        self.assertEqual(reveal_time_zero_counter, 2)

    def test_reveal_time_participant_consistence(self):
        '''test if reveal_time is consistent for two participant
        of the same exercise.
        '''
        exercise = create_exercise_20_emails()
        participant_1 = Participant.objects.create(exercise=exercise)
        participant_2 = Participant.objects.create(exercise=exercise)

        participant_1_emails = sorted(participant_1.exercise.emails, key=lambda email: email.id)
        participant_2_emails = sorted(participant_2.exercise.emails, key=lambda email: email.id)

        for pe_1, pe_2 in zip(participant_1_emails,participant_2_emails):
            self.assertEqual(pe_1.id,pe_2.id)
            self.assertEqual(pe_1.reveal_time, pe_2.reveal_time)


    def test_reveal_time_differ_for_exercises(self):
        '''test if reveal_time is different for the same emails
           belonging to two exercises. But sometimes it can happen,
           two emails belonging to different exercises can have the
           same reveal_time.
        '''
        exercises = create_two_exercises_20_emails()
        e_1_emails = sorted(exercises[0].emails, key=lambda email: email.id)
        e_2_emails = sorted(exercises[1].emails, key=lambda email: email.id)
        for email_exercise_1, email_exercise_2 in zip(e_1_emails,e_2_emails):
            self.assertEqual(email_exercise_1.id,email_exercise_2.id)
            self.assertNotEqual(email_exercise_1.reveal_time, email_exercise_2.reveal_time)


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
        #exercise.emails.add(email1)
        #I assume, by default, reveal_time = None. It can be changed depend on requrements
        exercise_emails_through = ExerciseEmailsThrough(exercise = exercise,
                                                        exerciseemail = email1)
        exercise_emails_through.save()






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