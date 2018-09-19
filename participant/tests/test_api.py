import uuid

from django.urls import reverse
from rest_framework import status

from phishtray.test.base import PhishtrayAPIBaseTest
from ..factories import ParticipantFactory
from exercise.factories import DemographicsInfoFactory


class ParticipantAPITests(PhishtrayAPIBaseTest):

    def setUp(self):
        super(ParticipantAPITests, self).setUp()
        self.participant = ParticipantFactory()
        # create questions and profile entries
        self.questions = DemographicsInfoFactory.create_batch(10)
        for q in self.questions:
            self.participant.exercise.demographics.add(q)
        self.participant.save()

    def test_update_participant_profile(self):
        url = reverse('api:participant-extend_profile', args=[self.participant.id])
        data = {
            'profile_form': [
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
            'profile_form': [
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
        self.assertListEqual([bad_id_1, bad_id_2], response.data['errors'][0]['id_list'])
        self.assertEqual(1, self.participant.profile.all().count())

    def test_update_participant_profile_missing_profile_form_data(self):
        url = reverse('api:participant-extend_profile', args=[self.participant.id])
        data = {
            # Note the spelling mistake / mismatch
            'profile_from_oops': [
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
