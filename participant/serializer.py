from rest_framework import serializers

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
