from django.db import models
from exercise.models import Exercise, ExerciseKey
import django.utils
import json


STARTED_EXPERIMENT = 0
COMPLETED_EXPERIMENT = 1
OTHER = 2

EVENT_TYPES = (
    (STARTED_EXPERIMENT, 'started'),
    (COMPLETED_EXPERIMENT, 'completed'),
    (OTHER, 'opened'),
)


class Participant(models.Model):

    def __str__(self):
        return "Participant: {} For: {}".format(self.id, self.exercise)

    id = models.AutoField(primary_key=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True)


class ParticipantProfile(models.Model):

    def __str__(self):
        return "{} {}:{}".format(self.participant, self.key, self.value)

    id = models.AutoField(primary_key=True)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    key = models.ForeignKey(ExerciseKey, on_delete=models.CASCADE)

    value = models.CharField(max_length=180, blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True)


class ParticipantAction(models.Model):

    def __str__(self):
        return self.id

    id = models.AutoField(primary_key=True)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    type = models.IntegerField(choices=EVENT_TYPES)

    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True)
