from django.test import TestCase

from exercise.models import *
from exercise.tests.helpers.assert_emal_response import *

class ExerciseEmailThreadTests(TestCase):

    def test_exercise_email_thread_not_found(self):
        response = self.client.get('/exercise/thread/1/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual((json.loads(response.content))['detail'], 'Not found.')

    def test_emails_thread_by_id(self):
        self.create_emails()

        response = self.client.get('/exercise/thread/1/')
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        self.assertCoverEmail(self, json_data)
        self.assertEmailResponseBody(self, json_data['emails'])

    @staticmethod
    def assertCoverEmail(self, json_data):
        self.assertEqual(1, json_data['id'])
        self.assertEqual('test email from unit test case', json_data['subject'])
        self.assertEqual('test@cybsafe.com', json_data['from_address'])
        self.assertEqual('Cybsafe Admin', json_data['from_name'])

    @staticmethod
    def assertEmailResponseBody(self, json_data):
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
            content="Hello world-2",
            belongs_to=email1
        )
        email2.save()
        email2.replies.add(replies)
        email2.attachments.add(attachment)