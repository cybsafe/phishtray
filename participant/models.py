from django.db import models
from exercise.models import Exercise
import django.utils
import json


class Participant(models.Model):

    def __str__(self):
        return self.title

    id = models.AutoField(primary_key=True)
    experiment = models.ForeignKey(Exercise)

    profile_json = models.TextField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True)

    @property
    def profile(self):
        """Returns profile object decoded from json."""
        if not self.review_json:
            return None
        return json.loads(self.review_json)

    def set_profile(self, profile):
        """Stores the dict as json in a field"""
        self.profile_json = json.dumps(profile)
