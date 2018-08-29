from django.test import TestCase
# from django.urls import reverse

from exercise.models import *
from exercise.tests.helpers.assert_email_response import *

import json


REPLY_PAYLOAD = {
  "milliseconds": 765432,
  "action": {
    "type": "email_reply",
    "associations": {
      "exerciseEmail": 1,
      "exerciseEmailReply": 1
    }
  }
}

ATTACHMENT_PAYLOAD = {
  "milliseconds": 567432,
  "action": {
    "type": "email_attachment_open",
    "associations": {
      "exerciseEmail": 1,
      "exerciseAttachment": 1
    }
  }
}

INVALID_PAYLOAD = {
  "milliseconds": 567432,
  "action": {
    "type": "invalid_type",
    "associations": {
      "exerciseEmail": 1,
      "exerciseAttachment": 1
    }
  }
}


class ExerciseEmailActionTests(TestCase):

    def test_exercise_email_action_json_invalid(self):
        response = self.client.post('/exercise/1/action/',
            json.dumps(INVALID_PAYLOAD),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 500)
        response_body = json.loads(response.content)
        self.assertEqual(response_body['message'], 'Json validation error')

    def test_exercise_email_action_email_invalid(self):
        response = self.client.post('/exercise/1/action/',
            json.dumps(REPLY_PAYLOAD),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 500)
        response_body = json.loads(response.content)
        self.assertEqual(response_body['message'], 'Invalid email id')

    def test_exercise_email_action_reply_invalid(self):
        self.create_email()
        response = self.client.post('/exercise/1/action/',
            json.dumps(REPLY_PAYLOAD),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 500)
        response_body = json.loads(response.content)
        self.assertEqual(response_body['message'], 'Invalid email reply id')

    def test_exercise_email_action_attachement_invalid(self):
        self.create_email()
        response = self.client.post('/exercise/1/action/',
            json.dumps(ATTACHMENT_PAYLOAD),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 500)
        response_body = json.loads(response.content)
        self.assertEqual(response_body['message'], 'Invalid attachement id')

    def test_exercise_email_action_reply_valid(self):
        self.create_email()
        self.create_email_reply()
        response = self.client.post('/exercise/1/action/',
            json.dumps(REPLY_PAYLOAD),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        exercise_action = ExerciseAction.objects.all()
        self.assertEqual(exercise_action.count(), 1)
        EmailAssertHelper.assert_email_action(self, REPLY_PAYLOAD, exercise_action.first())

    def test_exercise_email_action_attachement_valid(self):
        self.create_email()
        self.create_email_attachement()
        response = self.client.post('/exercise/1/action/',
            json.dumps(ATTACHMENT_PAYLOAD),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        exercise_action = ExerciseAction.objects.all()
        self.assertEqual(exercise_action.count(), 1)
        EmailAssertHelper.assert_email_action(self, ATTACHMENT_PAYLOAD, exercise_action.first())

    def create_email(self):
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

    def create_email_reply(self):
        self.create_email()
        replies = ExerciseEmailReply(
            id=1,
            reply_type=1,
            message='I have received your email-1'

        )
        replies.save()

    def create_email_attachement(self):
        self.create_email()
        attachment = ExerciseAttachment(
            id = 1,
            filename ='location of file name'
        )
        attachment.save()
