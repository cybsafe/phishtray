from django import forms
from django.contrib import admin

from .models import (
    DemographicsInfo,
    Exercise,
    ExerciseAttachment,
    ExerciseEmail,
    ExerciseEmailRevealTime,
    ExerciseEmailReply,
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


class ExerciseEmailRevealTimeAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'email', 'reveal_time')


admin.site.register(DemographicsInfo)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(ExerciseEmail)
admin.site.register(ExerciseEmailRevealTime, ExerciseEmailRevealTimeAdmin)
admin.site.register(ExerciseEmailReply)
admin.site.register(ExerciseAttachment)
admin.site.register(ExerciseURL)
admin.site.register(ExerciseWebPages)
