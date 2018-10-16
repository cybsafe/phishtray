import csv
import tempfile
from operator import itemgetter

from rest_framework import serializers

from exercise.models import ExerciseEmail, EXERCISE_EMAIL_PHISH
from .models import (
    Participant,
    ParticipantAction,
    ParticipantProfileEntry,
    ActionLog)


class ParticipantActionSerializer(serializers.ModelSerializer):
    action_details = serializers.SerializerMethodField()

    class Meta:
        model = ParticipantAction
        fields = ('id', 'action_details',)

    def get_action_details(self, participant_action):
        log_entries_queryset = ActionLog.objects.filter(action=participant_action)
        data = {}

        for entry in log_entries_queryset:
            data[entry.name] = entry.value

        return data


class ParticipantProfileEntrySerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ParticipantProfileEntry
        fields = ('id', 'question', 'answer',)

    def get_question(self, profile_entry):
        return profile_entry.question


class ParticipantSerializer(serializers.ModelSerializer):
    actions = serializers.SerializerMethodField(read_only=True)
    profile = ParticipantProfileEntrySerializer(read_only=True, many=True)

    class Meta:
        model = Participant
        fields = ('id', 'exercise', 'profile', 'actions',)

    def get_actions(self, participant):
        participant_actions_queryset = ParticipantAction.objects.filter(participant=participant)
        return ParticipantActionSerializer(participant_actions_queryset, many=True).data


class ParticipantCSVReportSerializer(serializers.ModelSerializer):
    csv = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Participant
        fields = ('id', 'exercise', 'csv')

    def get_csv(self, participant):
        participant_actions_queryset = ParticipantAction.objects.filter(participant=participant)
        serialized_actions = ParticipantActionSerializer(participant_actions_queryset, many=True).data

        email_uuids = {
            action['action_details']['email_id'] for action in serialized_actions
            if action['action_details'].get('email_id')
        }

        csv_row_master = {
            'email_subject': None,
            'email_id': None,
            'opened': None,
            'opened_time': None,
            'phish': None,
            'response_option': None,
            'reported': None,
            'reported_time': None,
            'deleted': None,
            'deleted_time': None,
            'clicked_link': None,
            'entered_details': None,
            'entered_details_time': None,
            'submitted_details': None,
            'submitted_details_time': None
        }
        csv_headers = list(csv_row_master.keys())
        csv_rows = []

        def recorded(action_type, actions):
            records = [
                action for action in actions
                if action['action_details'].get('action_type') == action_type
            ]
            return (len(records) > 0)

        def get_value(action_type, key, actions):
            records = [
                action for action in actions
                if action['action_details'].get('action_type') == action_type
            ]
            # # always get the latest entry ?
            # records = sorted(records, key=itemgetter('time_delta'), reverse=True)

            if not records:
                return None

            return records[0]['action_details'].get(key)

        for email_uuid in email_uuids:
            related_actions = [
                action for action in serialized_actions
                if action['action_details'].get('email_id') == email_uuid
            ]
            csv_row = csv_row_master.copy()
            email = ExerciseEmail.objects.get(pk=email_uuid)
            csv_row['email_subject'] = email.subject
            csv_row['email_id'] = email_uuid
            csv_row['opened'] = recorded('email_opened', related_actions)
            csv_row['opened_time'] = get_value('email_opened', 'time_delta', related_actions)
            csv_row['phish'] = (email.phish_type == EXERCISE_EMAIL_PHISH)
            csv_row['response_option'] = get_value('email_replied', 'response_id', related_actions)
            csv_row['reported'] = recorded('email_reported', related_actions)
            csv_row['reported_time'] = get_value('email_reported', 'time_delta', related_actions)
            csv_row['deleted'] = recorded('email_deleted', related_actions)
            csv_row['deleted_time'] = get_value('email_deleted', 'time_delta', related_actions)
            csv_row['clicked_link'] = recorded('email_link_clicked', related_actions)
            csv_row['entered_details'] = recorded('webpage_login_credentials_entered', related_actions)
            csv_row['entered_details_time'] = get_value('webpage_login_credentials_entered', 'time_delta', related_actions)
            csv_row['submitted_details'] = recorded('webpage_login_credentials_submitted', related_actions)
            csv_row['submitted_details_time'] = get_value('webpage_login_credentials_submitted', 'time_delta', related_actions)

            csv_rows.append(csv_row)

        # with tempfile.TemporaryFile(mode='w') as fp:
        #     writer = csv.DictWriter(fp, fieldnames=csv_headers)
        #     writer.writeheader()
        #     for row in csv_rows:
        #         writer.writerow(row)

        data = {
            'headers': csv_headers,
            'rows': csv_rows
        }

        return data





