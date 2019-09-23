from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['id', 'email', 'username', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + ( (None, {'fields': ('organization',)}), )

    def get_queryset(self, request, *args, **kwargs):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            organization = request.user.organization
            queryset = queryset.filter(organization=organization)
        return queryset
