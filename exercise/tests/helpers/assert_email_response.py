
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

    @staticmethod
    def assert_email_action(self, json_data, instance):
        self.assertEqual(json_data['action']['type'], instance.get_action_display())
        self.assertEqual(json_data['milliseconds'], instance.milliseconds)
        self.assertEqual(json_data['action']['associations']['exerciseEmail'], instance.email.id)
        if instance.get_action_display() == 'email_reply':
            self.assertEqual(json_data['action']['associations']['exerciseEmailReply'], instance.reply.id)
            self.assertEqual(instance.attachment, None)
        elif instance.get_action_display() == 'email_attachment_open':
            self.assertEqual(json_data['action']['associations']['exerciseAttachment'], instance.attachment.id)
            self.assertEqual(instance.reply, None)
