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
)

from .helpers import copy_exercise

register = template.Library()


class ExerciseAdminForm(forms.ModelForm):
    class Meta:
        model = Exercise
        exclude = []


class ExerciseAdmin(admin.ModelAdmin):
    form = ExerciseAdminForm
    list_display = ("id", "title", "description", "length_minutes", "created_date")
    readonly_fields = ("copied_from",)
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


class ExerciseEmailPropertiesAdmin(admin.ModelAdmin):
    list_display = ("exercise", "email", "reveal_time")


admin.site.register(DemographicsInfo)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(ExerciseEmail)
admin.site.register(ExerciseTask)
admin.site.register(EmailReplyTaskScore)
admin.site.register(ExerciseEmailProperties, ExerciseEmailPropertiesAdmin)
admin.site.register(ExerciseEmailReply)
admin.site.register(ExerciseFile)
admin.site.register(ExerciseWebPage)