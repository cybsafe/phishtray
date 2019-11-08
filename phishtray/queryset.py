from django.db.models import QuerySet
from users.models import User


class OrganizationQuerySet(QuerySet):
    def filter_by_org_private(self, user):

        if not user or not isinstance(user, User):
            return self.none()

        if not user.is_superuser:
            return self.filter(organization=user.organization, deleted_at=None)

        return self.filter(deleted_at=None)
