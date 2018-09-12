from .models import ParticipantAction, Participant
from exercise.models import Exercise, ExerciseEmail, ExerciseAttachment


@staticmethod
def log_action(type, user_data):
    participant = Participant.objects.get(pk=user_data.participant)
    experiment = Exercise.objects.get(pk=user_data.exercise)
    email = ExerciseEmail.objects.get(pk=user_data.email) if 'email' in user_data else None
    attachment = ExerciseAttachment.objects.get(pk=user_data.attachment) if 'attachment' in user_data else None
    action = ParticipantAction.create(
        type=type,
        participant=participant,
        experiment=experiment,
        email=email,
        attachment=attachment
    )
    action.save()
