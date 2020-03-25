import uuid

from django.apps import apps
from django.db import models
from django.db.models import QuerySet

from django.contrib import admin
from django.db.models import Manager


class MultiTenantQuerySet(QuerySet):
    def filter_by_org_private(self, user):
        User = apps.get_model("users", "User")

        if not user or not isinstance(user, User):
            return self.none()

        if not user.is_superuser:
            if user.organization is None:
                return self.none()
            else:
                return self.filter(organization=user.organization)

        return self

    def filter_by_org_public(self, user):

        if not user.is_superuser:
            public_orgs = self.filter(organization=None)
            if user.organization is None:
                return public_orgs
            else:
                private_orgs = self.filter(organization=user.organization)
                return private_orgs | public_orgs

        return self


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


class PhishtrayBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        abstract = True
