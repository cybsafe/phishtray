from django.db.models import QuerySet
from users.models import User


class ExerciseQuerySet(QuerySet):

    def filter_by_user(self, user):
        if not user.is_superuser:
            public_exercises = self.filter(organization=None)
            if user.organization is None:
                return public_exercises
            else:
                private_exercises = self.filter(organization=user.organization)
                return private_exercises | public_exercises
        else:
            return self

    def filter_by_org_private(self, user):
        if not user.is_superuser:
            return self.filter(organization=user.organization)
        else:
            return self


class ExerciseEmailPropertiesQuerySet(QuerySet):
    def filter_by_org_private(self, user):
        from .models import Exercise

        if not user or not isinstance(user, User):
            return self.none()

        if not user.is_superuser:
            return self.filter(
                exercise__in=Exercise.user_objects.filter_by_org_private(user=user)
            )
        return self
