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

from .helpers import copy_exercise, add_trial
from phishtray.base import MultiTenantModelAdmin

register = template.Library()


class ExerciseAdminForm(forms.ModelForm):
    class Meta:
        model = Exercise
        exclude = []


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    form = ExerciseAdminForm
    list_display = ("id", "title", "description", "length_minutes", "created_date")
    readonly_fields = (
        "copied_from",
        "updated_by",
        "published_by",
        "trial_version",
        "initial_trial",
    )
    change_form_template = "admin/exercise/change_form.html"
    ordering = ("-created_date",)

    def response_change(self, request, obj):
        if "_copy_exercise" in request.POST:
            exercise_copy = copy_exercise(obj, request.user)
            self.message_user(
                request, f"Exercise {exercise_copy.title} created successfully."
            )
            return redirect(
                reverse("admin:exercise_exercise_change", args=[exercise_copy.id])
            )

        if "_add_trial" in request.POST:
            exercise_trial = add_trial(obj, request.user)
            self.message_user(
                request, f"Exercise Trial {exercise_trial.title} created successfully."
            )
            return redirect(
                reverse("admin:exercise_exercise_change", args=[exercise_trial.id])
            )

        return super().response_change(request, obj)

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request))
        if not request.user.is_superuser:
            fields.append("organization")
        return fields

    def save_model(self, request, obj, form, change):
        # When creating a new exercise, it should have the
        # 'published by' and 'organization' fields filled in with the user information
        if not change:
            obj.published_by = request.user
            obj.organization = request.user.organization
        obj.updated_by = request.user
        obj.save()

    def get_queryset(self, request):
        return Exercise.user_objects.filter_by_user(user=request.user)

    def has_change_permission(self, request, obj=None):
        # Public exercises' permissions
        if obj.__class__.__name__ == "Exercise" and not obj.organization:
            if not request.user.is_superuser:
                if obj.published_by is None:
                    return False
                elif (
                    request.user.organization is not None
                    and request.user.organization == obj.published_by.organization
                ):
                    return True
            return True
        return super().has_change_permission(request, obj)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "demographics":
            kwargs["queryset"] = DemographicsInfo.objects.filter_by_org_private(
                user=request.user
            )
        elif db_field.name == "emails":
            kwargs["queryset"] = ExerciseEmail.objects.filter_by_org_private(
                user=request.user
            )
        elif db_field.name == "files":
            kwargs["queryset"] = ExerciseFile.objects.filter_by_org_private(
                user=request.user
            )

        return super().formfield_for_manytomany(db_field, request, **kwargs)


class ExerciseEmailPropertiesListFilter(admin.SimpleListFilter):
    title = "Exercise"
    parameter_name = "exercise"

    def lookups(self, request, model_admin):
        exercises = Exercise.user_objects.filter_by_org_private(request.user)
        return [(e.id, e) for e in exercises]

    def queryset(self, request, queryset):
        queryset = ExerciseEmailProperties.objects.filter_by_org_private(
            user=request.user
        )

        if self.value():
            return queryset.filter(exercise=self.value())
        else:
            return queryset


@admin.register(ExerciseEmailProperties)
class ExerciseEmailPropertiesAdmin(admin.ModelAdmin):
    list_display = ("exercise", "email", "reveal_time")
    list_filter = (ExerciseEmailPropertiesListFilter,)
    search_fields = ("email__subject",)

    def get_queryset(self, request):
        return ExerciseEmailProperties.objects.filter_by_org_private(user=request.user)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "release_codes":
            kwargs[
                "queryset"
            ] = ExerciseWebPageReleaseCode.objects.filter_by_org_private(
                user=request.user
            )
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "web_page":
            kwargs["queryset"] = ExerciseWebPage.objects.filter_by_org_private(
                user=request.user
            )
        elif db_field.name == "email":
            kwargs["queryset"] = ExerciseEmail.objects.filter_by_org_private(
                user=request.user
            )
        elif db_field.name == "exercise":
            kwargs["queryset"] = Exercise.user_objects.filter_by_org_private(
                user=request.user
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ExerciseWebPageReleaseCode)
class ExerciseWebPageReleaseCodeAdmin(MultiTenantModelAdmin):
    list_display = ("release_code",)

    def get_queryset(self, request):
        return ExerciseWebPageReleaseCode.objects.filter_by_org_private(
            user=request.user
        )


@admin.register(ExerciseWebPage)
class ExerciseWebPageAdmin(MultiTenantModelAdmin):
    def get_queryset(self, request):
        return ExerciseWebPage.objects.filter_by_org_private(user=request.user)


@admin.register(ExerciseEmail)
class ExerciseEmailAdmin(MultiTenantModelAdmin):
    def get_queryset(self, request):
        return ExerciseEmail.objects.filter_by_org_private(user=request.user)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "replies":
            kwargs["queryset"] = ExerciseEmailReply.objects.filter_by_org_private(
                user=request.user
            )
        elif db_field.name == "attachments":
            kwargs["queryset"] = ExerciseFile.objects.filter_by_org_private(
                user=request.user
            )
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "belongs_to":
            kwargs["queryset"] = ExerciseEmail.objects.filter_by_org_private(
                user=request.user
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ExerciseEmailReply)
class ExerciseEmailReplyAdmin(MultiTenantModelAdmin):
    def get_queryset(self, request):
        return ExerciseEmailReply.objects.filter_by_org_private(user=request.user)


@admin.register(ExerciseFile)
class ExerciseFileAdmin(MultiTenantModelAdmin):
    def get_queryset(self, request):
        return ExerciseFile.objects.filter_by_org_private(user=request.user)


@admin.register(DemographicsInfo)
class DemographicsInfoAdmin(MultiTenantModelAdmin):
    def get_queryset(self, request):
        return DemographicsInfo.objects.filter_by_org_private(user=request.user)


@admin.register(ExerciseTask)
class ExerciseTaskAdmin(MultiTenantModelAdmin):
    def get_queryset(self, request):
        return ExerciseTask.objects.filter_by_org_private(user=request.user)


@admin.register(EmailReplyTaskScore)
class EmailReplyTaskScoreAdmin(MultiTenantModelAdmin):
    def get_queryset(self, request):
        return EmailReplyTaskScore.objects.filter_by_org_private(user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "email_reply":
            kwargs["queryset"] = ExerciseEmailReply.objects.filter_by_org_private(
                user=request.user
            )
        elif db_field.name == "task":
            kwargs["queryset"] = ExerciseTask.objects.filter_by_org_private(
                user=request.user
            )

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
