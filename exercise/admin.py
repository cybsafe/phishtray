from django import forms, template
from django.contrib import admin
from django.http import HttpResponseRedirect
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

register = template.Library()


class ExerciseAdminForm(forms.ModelForm):
    class Meta:
        model = Exercise
        exclude = []


class ExerciseAdmin(admin.ModelAdmin):
    form = ExerciseAdminForm
    list_display = ("id", "title", "description", "length_minutes")
    readonly_fields = ("copied_from",)
    change_form_template = "admin/exercise/change_form.html"

    def response_change(self, request, obj):
        if "_copy_exercise" in request.POST:
            copied_from = Exercise.objects.get(pk=obj.id)
            obj.title = obj.title + " Copy"
            obj.copied_from = copied_from
            obj.id = None
            obj.save()

            self.message_user(request, f"Exercise {obj.title} created successfully.")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


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
