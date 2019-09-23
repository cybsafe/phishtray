from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['email', 'username', ]
    fieldsets = UserAdmin.fieldsets + ( (None, {'fields': ('organization',)}), )
    # ( (None, {'fields': ('bio',)}), )
