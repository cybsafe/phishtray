import uuid

from django.utils import timezone

from django.db import models
from django.db.models import QuerySet

from utils.cache import flush_cache
from django.contrib import admin
from users.models import User
from django.db.models import Manager


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop("alive_only", True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeletionModel(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True, editable=False)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super(SoftDeletionModel, self).delete()


class PhishtrayBaseModel(SoftDeletionModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        abstract = True


class CacheBusterMixin:
    """
    Use this mixin to flush the cache each time the instance is saved/deleted.
    """

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        flush_cache()

    # there's no need to override "delete"
    # as that will save the object which already triggers a flush

    def hard_delete(self):
        super().hard_delete()
        flush_cache()


class MultiTenantQuerySet(QuerySet):
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
        public_orgs = self.filter(organization=None, deleted_at=None)
        if not user.is_superuser:
            if user.organization is None:
                return public_orgs
            else:
                private_orgs = self.filter(
                    organization=user.organization, deleted_at=None
                )
                return private_orgs | public_orgs
        return self.filter(deleted_at=None)

    def filter_by_user(self, user):
        if not user or not isinstance(user, User):
            return self.none()

        if user.is_superuser:
            return self

        return self.filter(id=user.organization_id)


class MultiTenantManager(Manager.from_queryset(MultiTenantQuerySet)):
    pass


class MultiTenantMixin(models.Model):
    organization = models.ForeignKey(
        "participant.Organization", on_delete=models.PROTECT, null=True, blank=True
    )
    objects = MultiTenantManager()

    class Meta:
        abstract = True


class MultiTenantModelAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        ro_fields = list(super().get_readonly_fields(request))
        if not request.user.is_superuser:
            ro_fields.append("organization")
        return ro_fields

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and not obj.organization:
            obj.organization = request.user.organization

        super().save_model(request, obj, form, change)
