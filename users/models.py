from django.contrib.auth.models import AbstractUser

from phishtray.base import MultiTenantMixin
from users.managers import PhishtrayUserManager


class User(MultiTenantMixin, AbstractUser):
    objects = PhishtrayUserManager()

    def __str__(self):
        return "{self.id} {self.first_name} {self.last_name}, Organization: {self.organization}".format(
            self=self
        )
