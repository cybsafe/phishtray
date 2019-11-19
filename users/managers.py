from django.contrib.auth.models import UserManager

from phishtray.base import MultiTenantManager


class PhishtrayUserManager(MultiTenantManager, UserManager):
    pass
