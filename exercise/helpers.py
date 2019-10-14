from .models import Exercise


def copy_exercise(obj):
    """
    Create a copy of an Exercise
    :param obj: An Exercise instance
    :return: Another Exercise instance copied from the original one

    """
    original_exercise = Exercise.objects.get(pk=obj.id)

    obj.title = obj.title + " Copy"

    if not obj.copied_from:
        obj.copied_from = original_exercise

    obj.id = None
    obj.save()

    # Add ManyToMany connections
    obj.demographics.add(*original_exercise.demographics.all())
    obj.emails.add(*original_exercise.emails.all())
    obj.files.add(*original_exercise.files.all())

    return obj
