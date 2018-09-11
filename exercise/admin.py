from django import forms
from django.contrib import admin

from .models import (
    Exercise,
    ExerciseAttachment,
    ExerciseEmail,
    ExerciseEmailReply,
    ExerciseKey,
    ExerciseURL,
    ExerciseWebPages
)


class ExerciseAdminForm(forms.ModelForm):
    class Meta:
        model = Exercise
        exclude = []


class ExerciseAdmin(admin.ModelAdmin):
    form = ExerciseAdminForm
    list_display = ('id', 'title', 'description', 'length_minutes')


admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(ExerciseKey)
admin.site.register(ExerciseEmail)
admin.site.register(ExerciseEmailReply)
admin.site.register(ExerciseAttachment)
admin.site.register(ExerciseURL)
admin.site.register(ExerciseWebPages)
