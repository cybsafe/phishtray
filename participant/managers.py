from django.db.models import Manager
from .queryset import ParticipantQuerySet, OrganizationQuerySet


class ParticipantManager(Manager.from_queryset(ParticipantQuerySet)):
    pass


class OrganizationManager(Manager.from_queryset(OrganizationQuerySet)):
    pass
