from .models import Exercise


def copy_exercise(obj):
    # Create a copy of the Exercise
    original_exercise = Exercise.objects.get(pk=obj.id)
    obj.title = obj.title + " Copy"
    obj.id = None

    if not obj.copied_from:
        obj.copied_from = original_exercise
    obj.save()

    # Add ManyToMany connections
    obj.demographics.add(*original_exercise.demographics.all())
    obj.emails.add(*original_exercise.emails.all())
    obj.files.add(*original_exercise.files.all())

    return obj
