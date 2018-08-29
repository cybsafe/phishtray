
import json


class EmailAssertHelper:

    @staticmethod
    def assert_first_email(self, json_data):
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
    def assert_second_email(self, json_data):
        self.assertEqual(json_data['id'], 2)
        self.assertEqual(json_data['subject'], 'test email from unit test case-2')
        self.assertEqual(json_data['from_address'], 'test2@cybsafe.com')
        self.assertEqual(json_data['from_name'], 'Cybsafe Admin-2')
        self.assertEqual(json_data['to_address'], 'sendTo2@cybsafe.com')
        self.assertEqual(json_data['to_name'], 'Cybsafe Admin-2')
        self.assertEqual(json_data['phish_type'], 1)
        self.assertEqual(json_data['replies'][0]['id'], 1)
        self.assertEqual(json_data['replies'][0]['reply_type'], 1)
        self.assertEqual(json_data['replies'][0]['message'], 'I have received your email-1')
        self.assertEqual(json_data['attachments'][0]['id'], 1)
        self.assertEqual(json_data['attachments'][0]['filename'], 'location of file name')
