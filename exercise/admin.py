from django import forms
from django.contrib import admin
from .models import (
    DemographicsInfo,
    Exercise,
    ExerciseFile,
    ExerciseEmail,
    ExerciseEmailProperties,
    ExerciseEmailReply,
    ExerciseURL,
    ExerciseWebPages,
    ExerciseTask,
    EmailReplyTaskScore,
    Trial,
)


class ExerciseAdminForm(forms.ModelForm):
    class Meta:
        model = Exercise
        exclude = []


class ExerciseAdmin(admin.ModelAdmin):
    form = ExerciseAdminForm
    list_display = ("id", "title", "description", "length_minutes")


class ExerciseEmailPropertiesAdmin(admin.ModelAdmin):
    list_display = ("exercise", "email", "reveal_time")


class TrialAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "experiment")


admin.site.register(DemographicsInfo)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(ExerciseEmail)
admin.site.register(ExerciseTask)
admin.site.register(EmailReplyTaskScore)
admin.site.register(ExerciseEmailProperties, ExerciseEmailPropertiesAdmin)
admin.site.register(ExerciseEmailReply)
admin.site.register(ExerciseFile)
admin.site.register(ExerciseURL)
admin.site.register(ExerciseWebPages)
admin.site.register(Trial, TrialAdmin)
