from django.db.models import Manager
from .queryset import (
    ExerciseQuerySet,
    ExerciseEmailPropertiesQuerySet,
    ExerciseWebPageReleaseCodeQuerySet,
    ExerciseWebPageQuerySet,
)


class ExerciseManager(Manager.from_queryset(ExerciseQuerySet)):
    pass


class ExerciseEmailPropertiesManager(
    Manager.from_queryset(ExerciseEmailPropertiesQuerySet)
):
    pass


class ExerciseWebPageReleaseCodeManager(
    Manager.from_queryset(ExerciseWebPageReleaseCodeQuerySet)
):
    pass


class ExerciseWebPageManager(Manager.from_queryset(ExerciseWebPageQuerySet)):
    pass
