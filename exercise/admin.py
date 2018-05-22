from django.contrib import admin
from django import forms

from django.contrib import admin

from .models import Exercise


class ExerciseAdminForm(forms.ModelForm):
    class Meta:
        model = Exercise
        exclude = []

    readonly_fields = ['link',]


class ExerciseAdmin(admin.ModelAdmin):
    form = ExerciseAdminForm
    list_display = ('title', 'link', 'description', 'length_minutes')
    list_filter = ['id']


admin.site.register(Exercise, ExerciseAdmin)
