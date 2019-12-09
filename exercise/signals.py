from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from exercise.models import Exercise


@receiver(m2m_changed, sender=Exercise.emails.through)
def sync_exercise_email_properties(sender, instance, action, **kwargs):
    # Make sure to sync after the updates have been done to the relation
    if action in ("post_add", "post_remove", "post_clear"):
        instance.sync_email_properties()
