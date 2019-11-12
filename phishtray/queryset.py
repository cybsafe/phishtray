from django.db.models import QuerySet
from users.models import User


class OrganizationQuerySet(QuerySet):
    """
    Suppose to work with models which inherits from PhishtrayBaseModel
    or SoftDeletionModel
    """

    def filter_by_org_private(self, user):

        if not user or not isinstance(user, User):
            return self.none()

        if not user.is_superuser:
            return self.filter(organization=user.organization, deleted_at=None)

        return self.filter(deleted_at=None)

    def filter_by_org_public(self, user):
        public_orgs = self.filter(organisation=None, deleted_at=None)
        if not user.is_superuser:
            if user.organization is None:
                return public_orgs
            else:
                private_orgs = self.filter(
                    organisation=user.organization, deleted_at=None
                )
                return private_orgs | public_orgs
        return self.filter(deleted_at=None)
