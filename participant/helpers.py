from .models import Participant


def create_participant(exercise, trial=None):
    participant = Participant(exercise=exercise, trial=trial)
    participant.save()

    return participant
