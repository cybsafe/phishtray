from django.contrib import admin
from .models import Participant


@admin.register(Participant)
class ParticipantList(admin.ModelAdmin):
    list_filter = ("exercise",)
