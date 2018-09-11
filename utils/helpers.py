from hashids import Hashids
from django.conf import settings


hasher = Hashids(
        salt=settings.URLSALT,
        alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789',
        min_length=3,
)
