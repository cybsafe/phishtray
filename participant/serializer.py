from rest_framework import serializers
from datetime import datetime

from exercise.models import ExerciseEmail, EXERCISE_EMAIL_PHISH

from .models import ActionLog, Participant, ParticipantAction, ParticipantProfileEntry


class ParticipantActionSerializer(serializers.ModelSerializer):
    action_details = serializers.SerializerMethodField()

    class Meta:
        model = ParticipantAction
        fields = ("id", "action_details")

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
        fields = ("id", "question", "answer")

    def get_question(self, profile_entry):
        return profile_entry.question


class ParticipantSerializer(serializers.ModelSerializer):
    actions = serializers.SerializerMethodField(read_only=True)
    profile = ParticipantProfileEntrySerializer(read_only=True, many=True)

    class Meta:
        model = Participant
        fields = ("id", "exercise", "profile", "actions")

    def get_actions(self, participant):
        participant_actions_queryset = ParticipantAction.objects.filter(
            participant=participant
        )
        return ParticipantActionSerializer(participant_actions_queryset, many=True).data


class ParticipantActionLogDownloadCSVSerializer(serializers.ModelSerializer):
    download_csv_url = serializers.SerializerMethodField()
    profile = ParticipantProfileEntrySerializer(read_only=True, many=True)

    class Meta:
        model = Participant
        fields = ("id", "download_csv_url", "profile")

    def get_download_csv_url(self, participant):
        req = self.context.get("request")
        url = "{0}://{1}{2}download-csv?participant={3}".format(
            req.scheme, req.get_host(), req.path, participant.id
        )
        return url


class ParticipantActionLogToCSVSerializer(serializers.ModelSerializer):
    csv = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Participant
        fields = ("id", "exercise", "csv")

    def get_csv(self, participant):
        participant_actions_queryset = ParticipantAction.objects.filter(
            participant=participant
        )
        serialized_actions = ParticipantActionSerializer(
            participant_actions_queryset, many=True
        ).data

        email_uuids = {
            action["action_details"]["email_id"]
            for action in serialized_actions
            if action["action_details"].get("email_id")
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
                action
                for action in actions
                if action["action_details"].get("action_type") == action_type
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
                action
                for action in actions
                if action["action_details"].get("action_type") == action_type
            ]
            # TODO: always get the latest entry of the given action_type?
            # records = sorted(records, key=itemgetter('time_delta'), reverse=True)

            if not records:
                return None

            return records[0]["action_details"].get(key)

        def get_value_in_seconds(action_type, key, actions):
            """
            Helps to retrieve a value from actions and then turn into a readable time format.
            :param action_type: string
                - action type to search for
            :param key: string
                - dict key to look up
            :param actions: list
                - list of action dicts
            :return: value
                - returns the value of the timestamp as a minute:second format or None
            """
            timestamp = get_value(action_type, key, actions)

            if not timestamp:
                return None

            timestamp = int(timestamp)
            return datetime.fromtimestamp(timestamp/1000).strftime('%M:%S')

        csv_row_master = {
            "email_subject": None,
            "email_id": None,
            "opened": None,
            "opened_time": None,
            "phish": None,
            "response_option": None,
            "response_time": None,
            "reply_button_clicked": None,
            "replied_time": None,
            "report_button_clicked": None,
            "reported_time": None,
            "delete_button_clicked": None,
            "deleted_time": None,
            "forward_button_clicked": None,
            "forwarded_time": None,
            "clicked_link": None,
            "entered_details": None,
            "entered_details_time": None,
            "submitted_details": None,
            "submitted_details_time": None,
            "prolific_id": participant.pid,
        }
        csv_row_dicts = []

        for email_uuid in email_uuids:
            related_actions = [
                action
                for action in serialized_actions
                if action["action_details"].get("email_id") == email_uuid
            ]
            csv_row = csv_row_master.copy()

            try:
                email = ExerciseEmail.objects.get(pk=email_uuid)
            except ExerciseEmail.DoesNotExist:
                # Looks like someone has deleted the email
                # so exclude it from the CSV
                continue

            csv_row["email_subject"] = email.subject
            csv_row["email_id"] = email_uuid
            csv_row["opened"] = recorded("email_opened", related_actions)
            csv_row["opened_time"] = get_value_in_seconds(
                "email_opened", "time_delta", related_actions
            )
            csv_row["phish"] = email.phish_type == EXERCISE_EMAIL_PHISH
            csv_row["response_option"] = get_value(
                "email_quick_reply", "message", related_actions
            )
            csv_row["response_time"] = get_value_in_seconds(
                "email_quick_reply", "time_delta", related_actions
            )
            csv_row["reply_button_clicked"] = recorded("email_replied", related_actions)
            csv_row["replied_time"] = get_value_in_seconds(
                "email_replied", "time_delta", related_actions
            )
            csv_row["report_button_clicked"] = recorded(
                "email_reported", related_actions
            )
            csv_row["reported_time"] = get_value_in_seconds(
                "email_reported", "time_delta", related_actions
            )
            csv_row["delete_button_clicked"] = recorded(
                "email_deleted", related_actions
            )
            csv_row["deleted_time"] = get_value_in_seconds(
                "email_deleted", "time_delta", related_actions
            )
            # forwarded
            csv_row["forward_button_clicked"] = recorded(
                "email_forwarded", related_actions
            )
            csv_row["forwarded_time"] = get_value_in_seconds(
                "email_forwarded", "time_delta", related_actions
            )
            csv_row["clicked_link"] = recorded("email_link_clicked", related_actions)
            csv_row["entered_details"] = recorded(
                "webpage_login_credentials_entered", related_actions
            )
            csv_row["entered_details_time"] = get_value_in_seconds(
                "webpage_login_credentials_entered", "time_delta", related_actions
            )
            csv_row["submitted_details"] = recorded(
                "webpage_login_credentials_submitted", related_actions
            )
            csv_row["submitted_details_time"] = get_value_in_seconds(
                "webpage_login_credentials_submitted", "time_delta", related_actions
            )

            csv_row_dicts.append(csv_row)

        csv_headers = list(csv_row_master.keys())
        csv_rows = []

        for row in csv_row_dicts:
            csv_rows.append([str(v) for v in row.values()])

        data = {"headers": csv_headers, "rows": csv_rows}

        return data


class ParticipantScoreSerializer(serializers.ModelSerializer):
    scores = serializers.SerializerMethodField()
    phishing_emails = serializers.SerializerMethodField()
    training_link = serializers.SerializerMethodField()
    debrief = serializers.SerializerMethodField()

    def get_phishing_emails(self, participant):
        emails_list = list(
            ExerciseEmail.objects.filter(
                exercise__participant=participant, phish_type=EXERCISE_EMAIL_PHISH
            ).values("id", "subject", "from_address", "content", "phishing_explained")
        )

        for email in emails_list:
            email["participant_behaviour"], email[
                "participant_actions"
            ] = participant.phishing_email_behaviour_and_actions(str(email["id"]))

        return emails_list

    def get_training_link(self, participant):
        return participant.exercise.training_link

    def get_debrief(self, participant):
        return participant.exercise.debrief

    def get_scores(self, participant):
        return participant.scores

    class Meta:
        model = Participant
        fields = ("id", "scores", "phishing_emails", "debrief", "training_link")
