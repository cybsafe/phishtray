from django.contrib import admin
from django import forms

from django.contrib import admin

from .models import Exercise, ExerciseKey, ExerciseEmail, ExerciseAttachment, ExerciseEmailReply


class ExerciseAdminForm(forms.ModelForm):
    class Meta:
        model = Exercise
        exclude = []

    readonly_fields = ['link',]


class ExerciseAdmin(admin.ModelAdmin):
    form = ExerciseAdminForm
    list_display = ('id', 'title', 'link', 'description', 'length_minutes')
    list_filter = ['id']


admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(ExerciseKey)
admin.site.register(ExerciseEmail)
admin.site.register(ExerciseEmailReply)
admin.site.register(ExerciseAttachment)
