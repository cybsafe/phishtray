from django.db.models import Manager
from .queryset import OrganizationQuerySet


class OrganizationManager(Manager.from_queryset(OrganizationQuerySet)):
    pass
