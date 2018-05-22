from django.db import models

from utils import helpers
import django.utils
import json
import uuid


class Exercise(models.Model):

    def __str__(self):
        return self.title

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    introduction = models.TextField(null=True, blank=True)
    afterword = models.TextField(null=True, blank=True)

    length_minutes = models.IntegerField()

    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True)

    profile_definition_json = models.TextField(null=True, blank=True)

    @property
    def profile_definition(self):
        """Returns profile object decoded from json."""
        if not self.review_json:
            return None
        return json.loads(self.review_json)

    def set_profile_definition(self, profile):
        """Stores the dict as json in a field"""
        self.profile_json = json.dumps(profile)

    @property
    def link(self):
        return helpers.hasher.encode(self.id)
