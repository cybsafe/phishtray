from django.contrib.auth.models import AbstractUser

from django.db import models

from .managers import PhishtrayUserManager


class User(AbstractUser):
    organization = models.ForeignKey(
        "participant.Organization", null=True, blank=True, on_delete=models.DO_NOTHING
    )

    objects = PhishtrayUserManager()
