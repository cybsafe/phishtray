from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = ["id", "email", "username", "first_name", "last_name"]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("organization",)}),)

    def get_queryset(self, request):
        return User.objects.filter_by_user(user=request.user)
