from django.db import models
from exercise.models import (
    DemographicsInfo,
    Exercise,
    ExerciseEmail,
    ExerciseAttachment,
)
from phishtray.base import PhishtrayBaseModel

STARTED_EXPERIMENT = 0
COMPLETED_EXPERIMENT = 1
OPENED_EMAIL = 2
OPENED_UNSAFE_EMAIL_LINK = 3
DOWNLOADED_UNSAFE_EMAIL_ATTACHMENT = 4

EVENT_TYPES = (
    (STARTED_EXPERIMENT, 'started'),
    (COMPLETED_EXPERIMENT, 'completed'),
    (OPENED_EMAIL, 'opened'),
    (OPENED_UNSAFE_EMAIL_LINK, 'unsafe_link'),
    (DOWNLOADED_UNSAFE_EMAIL_ATTACHMENT, 'unsafe_attachment'),
)


class ActionLog(PhishtrayBaseModel):
    """
    Simple key/value entries representing Participant actions.
    """
    name = models.CharField(max_length=255, blank=False, null=False)
    value = models.CharField(max_length=500, blank=False, null=False)


class ParticipantAction(PhishtrayBaseModel):
    """
    Groups a set of ActionLogs together.
    """
    action_logs = models.ManyToManyField(ActionLog, editable=False)


class ParticipantProfileEntry(PhishtrayBaseModel):
    """
    Aggregates Demographic Info
    """
    demographics_info = models.ForeignKey(DemographicsInfo, on_delete=models.PROTECT)
    answer = models.CharField(max_length=180, blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.demographics_info.question, self.answer)


class Participant(PhishtrayBaseModel):

    def __str__(self):
        return 'Participant: {} For: {}'.format(self.id, self.exercise)

    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
    actions = models.ManyToManyField(ParticipantAction)
    profile = models.ManyToManyField(ParticipantProfileEntry)
