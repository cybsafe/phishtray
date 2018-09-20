import uuid

from django.urls import reverse
from rest_framework import status

from participant.models import ActionLog
from phishtray.test.base import PhishtrayAPIBaseTest
from ..factories import ParticipantFactory
from exercise.factories import DemographicsInfoFactory


class ParticipantProfileAPITests(PhishtrayAPIBaseTest):

    def setUp(self):
        super(ParticipantProfileAPITests, self).setUp()
        self.participant = ParticipantFactory()
        # create questions and profile entries
        self.questions = DemographicsInfoFactory.create_batch(10)
        for q in self.questions:
            self.participant.exercise.demographics.add(q)
        self.participant.save()

    def test_update_participant_profile(self):
        url = reverse('api:participant-extend_profile', args=[self.participant.id])
        data = {
            'profileForm': [
                {
                    'id': self.questions[0].id,
                    'value': '20'
                },
                {
                    'id': self.questions[2].id,
                    'value': 'Some text'
                }
            ]
        }

        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('Participant profile has been successfully updated.',
                         response.data.get('message'))
        self.assertEqual(2, self.participant.profile.all().count())

    def test_partial_update_participant_profile(self):
        url = reverse('api:participant-extend_profile', args=[self.participant.id])
        bad_id_1 = str(uuid.uuid4())
        bad_id_2 = str(uuid.uuid4())
        data = {
            'profileForm': [
                {
                    'id': bad_id_1,
                    'value': '20'
                },
                {
                    'id': bad_id_2,
                    'value': 'wibble wobble'
                },
                {
                    'id': self.questions[2].id,
                    'value': 'Some text'
                }
            ]
        }

        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('Participant profile has been partially updated due to errors.',
                         response.data.get('message'))
        self.assertEqual('Missing or invalid demographics IDs.',
                         response.data['errors'][0]['message'])
        self.assertListEqual([bad_id_1, bad_id_2], response.data['errors'][0]['idList'])
        self.assertEqual(1, self.participant.profile.all().count())

    def test_update_participant_profile_missing_profile_form_data(self):
        url = reverse('api:participant-extend_profile', args=[self.participant.id])
        data = {
            # Note the spelling mistake / mismatch
            'profileFromOops': [
                {
                    'id': self.questions[0].id,
                    'value': '20'
                },
                {
                    'id': self.questions[2].id,
                    'value': 'Some text'
                }
            ]
        }

        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(0, self.participant.profile.all().count())


class ParticipantActionsAPITests(PhishtrayAPIBaseTest):

    def setUp(self):
        super(ParticipantActionsAPITests, self).setUp()
        self.participant = ParticipantFactory()

    def test_add_participant_action(self):
        url = reverse('api:participant-action', args=[self.participant.id])
        data = {
            'action_type': 'SOME_ACTION_TYPE',
            'key1': 1234,
            'key2': 'some value',
            'key3': 'wibble wobble'
        }

        response = self.client.post(url, data)
        action_id = response.data.get('action_id')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('Action has been logged successfully.', response.data.get('message'))
        self.assertEqual(4, ActionLog.objects.filter(action__id=action_id).count())

    def test_add_participant_action_skip_complex_datatypes(self):
        url = reverse('api:participant-action', args=[self.participant.id])
        data = {
            'action_type': 'SOME_ACTION_TYPE',
            'key1': 1234,
            'key2': 'some value',
            'just_a_list': ['t', 'e', 's', 't'],
            'just_a_dict': {
                'wibble': 1,
                'wobble': 2,
                'another_list': [1, 2, 3, 4]
            }
        }

        response = self.client.post(url, data)
        action_id = response.data.get('action_id')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('Action has been partially logged. Cannot log complex data types.',
                         response.data.get('message'))
        self.assertListEqual(['just_a_list', 'just_a_dict'], response.data.get('skipped'))
        self.assertEqual(3, ActionLog.objects.filter(action__id=action_id).count())

    def test_add_participant_action_convert_keys_to_snake_case(self):
        url = reverse('api:participant-action', args=[self.participant.id])
        data = {
            'actionType': 'SOME_ACTION_TYPE',
            'myKeyOne': 1234,
        }

        response = self.client.post(url, data)
        action_id = response.data.get('action_id')
        action_names = [al.name for al in ActionLog.objects.filter(action__id=action_id)]

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('Action has been logged successfully.', response.data.get('message'))
        self.assertEqual(2, ActionLog.objects.filter(action__id=action_id).count())
        self.assertListEqual(['action_type', 'my_key_one'], sorted(action_names))

    def test_add_participant_action_nothing_to_log(self):
        url = reverse('api:participant-action', args=[self.participant.id])
        data = {}

        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('Nothing to log.', response.data.get('message'))
