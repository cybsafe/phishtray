from django.contrib import admin
from .models import Participant


class ParticipantList(admin.ModelAdmin):
    list_filter = ("exercise",)


admin.site.register(Participant, ParticipantList)
