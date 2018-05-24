from django.db import models

from utils import helpers
import django.utils
import json
import uuid


KEY_TYPE_INTEGER = 0
KEY_TYPE_TEXT = 1

EXERCISE_KEY_TYPES = (
    (KEY_TYPE_INTEGER, 'number'),
    (KEY_TYPE_TEXT, 'text'),
)


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


class ExerciseKey(models.Model):
    def __str__(self):
        return self.key

    id = models.AutoField(primary_key=True)
    exercise = models.ManyToManyField(Exercise)

    type = models.IntegerField(choices=EXERCISE_KEY_TYPES)
    key = models.CharField(max_length=180, blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True)

    @property
    def html5_type(self):
        return EXERCISE_KEY_TYPES[self.type][1]
