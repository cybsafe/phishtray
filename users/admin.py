from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from phishtray.base import MultiTenantModelAdmin
from .models import User

from django.utils.translation import ugettext_lazy as _


@admin.register(User)
class CustomUserAdmin(MultiTenantModelAdmin, UserAdmin):

    list_display = [
        "id",
        "email",
        "username",
        "first_name",
        "last_name",
        "organization",
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("organization",)}),)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        if request.user.is_superuser:
            perm_fields = (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        else:
            # modify these to suit the fields you want your
            # staff user to be able to edit
            perm_fields = ("is_active", "is_staff", "groups", "user_permissions")

        return [
            (None, {"fields": ("username", "password")}),
            (
                _("Personal info"),
                {"fields": ("first_name", "last_name", "email", "organization")},
            ),
            (_("Permissions"), {"fields": perm_fields}),
            (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        ]

    def get_queryset(self, request):
        return User.objects.filter_by_org_private(user=request.user)

    def has_add_permission(self, request):
        if not request.user.is_superuser and not request.user.organization:
            return False

        return super().has_add_permission(request)
