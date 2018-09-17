from django.db import models
from django.core.exceptions import ValidationError
from exercise.models import Exercise, ExerciseKey, ExerciseEmail, ExerciseAttachment

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

from phishtray.base import PhishtrayBaseModel


class Participant(PhishtrayBaseModel):

    def __str__(self):
        return "Participant: {} For: {}".format(self.id, self.exercise)

    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)


class ParticipantProfile(PhishtrayBaseModel):

    def __str__(self):
        return "{} {}:{}".format(self.participant, self.key, self.value)

    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    key = models.ForeignKey(ExerciseKey, on_delete=models.CASCADE)
    value = models.CharField(max_length=180, blank=True, null=True)


class ParticipantAction(PhishtrayBaseModel):

    def __str__(self):
        return self.id

    @property
    def action_logs(self): ActionLog.objects.filter(action_id=self.id)

    # action log shouldn't be modified
    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError("You may not edit an existing %s" % self._meta.model_name)
        super(ParticipantAction, self).save(*args, **kwargs)


class ActionLog(PhishtrayBaseModel):

    def __str__(self):
        return self.id

    action_id = models.ForeignKey(ParticipantAction, blank=False, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, null=False)
    value = models.CharField(max_length=500, blank=False, null=False)
