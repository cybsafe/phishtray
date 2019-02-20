from rest_framework import serializers

from exercise.models import (
    ExerciseEmail,
    EXERCISE_EMAIL_PHISH,
)

from .models import (
    ActionLog,
    Participant,
    ParticipantAction,
    ParticipantProfileEntry,
)


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


class ParticipantActionLogDownloadCSVSerializer(serializers.ModelSerializer):
    download_csv_url = serializers.SerializerMethodField()
    profile = ParticipantProfileEntrySerializer(read_only=True, many=True)

    class Meta:
        model = Participant
        fields = ('id', 'download_csv_url', 'profile')

    def get_download_csv_url(self, participant):
        req = self.context.get('request')
        url = '{0}://{1}{2}download-csv?participant={3}'.format(req.scheme, req.get_host(), req.path, participant.id)
        return url


class ParticipantActionLogToCSVSerializer(serializers.ModelSerializer):
    csv = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Participant
        fields = ('id', 'exercise', 'csv')

    def get_csv(self, participant):
        participant_actions_queryset = ParticipantAction.objects.filter(participant=participant)
        serialized_actions = ParticipantActionSerializer(
            participant_actions_queryset, many=True).data

        email_uuids = {
            action['action_details']['email_id'] for action in serialized_actions
            if action['action_details'].get('email_id')
        }

        def recorded(action_type, actions):
            """
            Helps to identify if an action has been logged.
            :param action_type: string
                - action type to search for
            :param actions: list
                - list of action dicts
            :return: bool
                - whether action_type was found in actions
            """
            records = [
                action for action in actions
                if action['action_details'].get('action_type') == action_type
            ]
            return len(records) > 0

        def get_value(action_type, key, actions):
            """
            Helps to retrieve a value from actions.
            :param action_type: string
                - action type to search for
            :param key: string
                - dict key to look up
            :param actions: list
                - list of action dicts
            :return: value
                - returns the value of the dictionary key or None
            """
            records = [
                action for action in actions
                if action['action_details'].get('action_type') == action_type
            ]
            # TODO: always get the latest entry of the given action_type?
            # records = sorted(records, key=itemgetter('time_delta'), reverse=True)

            if not records:
                return None

            return records[0]['action_details'].get(key)

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
        csv_row_dicts = []

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
            csv_row['entered_details'] = recorded(
                'webpage_login_credentials_entered', related_actions)
            csv_row['entered_details_time'] = get_value(
                'webpage_login_credentials_entered', 'time_delta', related_actions)
            csv_row['submitted_details'] = recorded(
                'webpage_login_credentials_submitted', related_actions)
            csv_row['submitted_details_time'] = get_value(
                'webpage_login_credentials_submitted', 'time_delta', related_actions)

            csv_row_dicts.append(csv_row)

        csv_headers = list(csv_row_master.keys())
        csv_rows = []

        for row in csv_row_dicts:
            csv_rows.append(
                [str(v) for v in row.values()]
            )

        data = {
            'headers': csv_headers,
            'rows': csv_rows
        }

        return data


class ParticipantScoreSerializer(serializers.ModelSerializer):
    scores = serializers.SerializerMethodField()

    class Meta:
        model = Participant
        fields = ('id', 'scores')

    def get_scores(self, participant):
        return participant.scores
