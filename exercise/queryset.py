from django.db.models import QuerySet
from users.models import User


class ExerciseQuerySet(QuerySet):
    def filter_by_user(self, user):
        public_exercises = self.filter(organisation=None, deleted_at=None)
        if not user.is_superuser:
            if user.organization is None:
                return public_exercises
            else:
                private_exercises = self.filter(
                    organisation=user.organization, deleted_at=None
                )
                return private_exercises | public_exercises
        return self.filter(deleted_at=None)

    def filter_by_org_private(self, user):
        if not user.is_superuser:
            return self.filter(organisation=user.organization, deleted_at=None)
        return self.filter(deleted_at=None)


class ExerciseEmailPropertiesQuerySet(QuerySet):
    def filter_by_user(self, user):
        from .models import Exercise

        if not user or not isinstance(user, User):
            return self.none()

        if not user.is_superuser:
            return self.filter(
                exercise__in=Exercise.user_objects.filter_by_user(user=user)
            )
        return self


class ExerciseWebPageReleaseCodeQuerySet(QuerySet):
    def filter_by_user(self, user):
        from .models import ExerciseEmailProperties

        if not user or not isinstance(user, User):
            return self.none()

        if not user.is_superuser:
            codes = list(
                ExerciseEmailProperties.objects.filter_by_user(user=user)
                .values_list("release_codes__release_code", flat=True)
                .distinct()
            )
            return self.filter(release_code__in=codes)

        return self
