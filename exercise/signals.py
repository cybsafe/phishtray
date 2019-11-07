from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from exercise.models import Exercise


@receiver(m2m_changed, sender=Exercise.emails.through)
def sync_exercise_email_properties(sender, instance, **kwargs):
    instance.sync_email_properties()
