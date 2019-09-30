from .models import Participant
from exercise.models import Trial


def create_participant(exercise, trial=None):
    if trial is not None:
        trial = Trial.objects.get(pk=trial)
    participant = Participant(exercise=exercise, trial=trial)
    participant.save()

    return participant
