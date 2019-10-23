from django.db.models import Manager
from .queryset import ExerciseQuerySet


class ExerciseManager(Manager.from_queryset(ExerciseQuerySet)):
    pass
