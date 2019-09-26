from django.db.models import Manager
from django.contrib.auth.models import UserManager

from .queryset import UserQuerySet


class PhishtrayUserManager(UserManager, Manager.from_queryset(UserQuerySet)):
    pass
