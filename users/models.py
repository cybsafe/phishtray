from django.contrib.auth.models import AbstractUser

from django.db import models

from .managers import PhishtrayUserManager


class User(AbstractUser):
    organization = models.ForeignKey(
        "participant.Organization", null=True, blank=True, on_delete=models.DO_NOTHING
    )

    objects = PhishtrayUserManager()

    def __str__(self):
        return "{self.id} {self.first_name} {self.last_name}, Organisation: {self.organization}".format(
            self=self
        )
