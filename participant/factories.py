import factory

from exercise.factories import DemographicsInfoFactory, ExerciseFactory
from .models import ActionLog, Participant, ParticipantAction, ParticipantProfileEntry


class ProfileEntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ParticipantProfileEntry

    demographics_info = factory.SubFactory(DemographicsInfoFactory)
    answer = factory.Sequence(lambda n: "Answer {}".format(n + 1))


class ParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Participant

    exercise = factory.SubFactory(ExerciseFactory)


class ParticipantActionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ParticipantAction

    participant = factory.SubFactory(ParticipantFactory)


class ActionLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ActionLog

    action = factory.SubFactory(ParticipantActionFactory)
