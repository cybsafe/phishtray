from django import forms, template
from django.contrib import admin
from django.urls import reverse
from django.shortcuts import redirect
from .models import (
    DemographicsInfo,
    Exercise,
    ExerciseFile,
    ExerciseEmail,
    ExerciseEmailProperties,
    ExerciseEmailReply,
    ExerciseWebPage,
    ExerciseTask,
    EmailReplyTaskScore,
    ExerciseWebPageReleaseCode,
)

from .helpers import copy_exercise

register = template.Library()


class ExerciseAdminForm(forms.ModelForm):
    class Meta:
        model = Exercise
        exclude = []


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    form = ExerciseAdminForm
    list_display = ("id", "title", "description", "length_minutes", "created_date")
    readonly_fields = ("copied_from", "updated_by", "published_by")
    change_form_template = "admin/exercise/change_form.html"
    ordering = ("-created_date",)

    def response_change(self, request, obj):
        if "_copy_exercise" in request.POST:
            exercise_copy = copy_exercise(obj)
            self.message_user(
                request, f"Exercise {exercise_copy.title} created successfully."
            )
            return redirect(
                reverse("admin:exercise_exercise_change", args=[exercise_copy.id])
            )
        return super().response_change(request, obj)

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request))
        if not request.user.is_superuser:
            fields.append("organisation")
        return fields

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        obj.save()

    def get_queryset(self, request):
        return Exercise.user_objects.filter_by_user(user=request.user)

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if obj is None:
                print("No Obj: Guessing this is the list.")
                return True
            elif obj.published_by is None:
                print("published by is none: Only superusers can edit.")
                return False
            elif (
                request.user.organization is not None
                and request.user.organization == obj.published_by.organization
            ):
                print(
                    "Published by not none: Only admins for the exercise organisation or superusers can edit"
                )
                return True
        return True


@admin.register(ExerciseEmailProperties)
class ExerciseEmailPropertiesAdmin(admin.ModelAdmin):
    list_display = ("exercise", "email", "reveal_time")
    list_filter = ("exercise",)
    search_fields = ("email__subject",)


@admin.register(ExerciseWebPageReleaseCode)
class ExerciseWebPageReleaseCodeAdmin(admin.ModelAdmin):
    list_display = ("release_code",)


admin.site.register(DemographicsInfo)
admin.site.register(ExerciseEmail)
admin.site.register(ExerciseTask)
admin.site.register(EmailReplyTaskScore)
admin.site.register(ExerciseEmailReply)
admin.site.register(ExerciseFile)
admin.site.register(ExerciseWebPage)
