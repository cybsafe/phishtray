from django.db.models import Manager

from .queryset import OrganizationQuerySet, ParticipantQuerySet


class OrganizationManager(Manager.from_queryset(OrganizationQuerySet)):
    pass


class ParticipantManager(Manager.from_queryset(ParticipantQuerySet)):
    pass
