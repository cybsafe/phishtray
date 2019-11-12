from django.db.models import Manager

from .queryset import ParticipantQuerySet


class ParticipantManager(Manager.from_queryset(ParticipantQuerySet)):
    pass
