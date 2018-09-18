from django.urls import reverse
from rest_framework import serializers
from rest_framework.decorators import action

from .models import (
    Participant,
    ParticipantAction,
    ParticipantProfileEntry
)


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ('id', 'exercise', 'profile', 'actions')
