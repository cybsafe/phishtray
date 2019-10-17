from django.db.models import QuerySet


class ExerciseQuerySet(QuerySet):
    def filter_by_user(self, user):
        public_exercises = self.filter(organisation=None)
        if not user.is_superuser:
            if user.organization is None:
                return public_exercises
            else:
                private_exercises = self.filter(organisation=user.organization)
                return private_exercises | public_exercises
        return self
