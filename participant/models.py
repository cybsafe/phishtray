from django.db import models
from django.core.exceptions import ValidationError
from exercise.models import Exercise, ExerciseKey, ExerciseEmail

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
    participant = models.ForeignKey(Participant, on_delete=models.SET_NULL, null=True)
    experiment = models.ForeignKey(Exercise, on_delete=models.CASCADE, null=True)
    email = models.ForeignKey(ExerciseEmail, on_delete=models.CASCADE, null=True)

    type = models.IntegerField(choices=EVENT_TYPES)

    created_date = models.DateTimeField(auto_now_add=True, blank=True)

    # action log shouldn't be modified
    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError("You may not edit an existing %s" % self._meta.model_name)
        super(ParticipantAction, self).save(*args, **kwargs)
