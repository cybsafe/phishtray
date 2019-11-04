from django.db.models import Manager
from .queryset import ExerciseQuerySet, ExerciseEmailPropertiesQuerySet


class ExerciseManager(Manager.from_queryset(ExerciseQuerySet)):
    pass


class ExerciseEmailPropertiesManager(
    Manager.from_queryset(ExerciseEmailPropertiesQuerySet)
):
    pass
