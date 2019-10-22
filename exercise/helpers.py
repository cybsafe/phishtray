from .models import Exercise


def copy_exercise(original_exercise, current_user):
    """
    Create a copy of an Exercise
    :param original_exercise: An Exercise instance
    :return: Another Exercise instance copied from the original one

    """
    new_exercise = Exercise(
        title=original_exercise.title + " Copy",
        description=original_exercise.description,
        introduction=original_exercise.introduction,
        afterword=original_exercise.afterword,
        length_minutes=original_exercise.length_minutes,
        training_link=original_exercise.training_link,
        debrief=original_exercise.debrief,
        copied_from=original_exercise.copied_from,
        organisation=current_user.organization,
        published_by=current_user,
        updated_by=current_user,
    )

    if not original_exercise.copied_from:
        new_exercise.copied_from = original_exercise
    new_exercise.save()

    new_exercise.demographics.add(*original_exercise.demographics.all())
    new_exercise.emails.add(*original_exercise.emails.all())
    new_exercise.files.add(*original_exercise.files.all())

    return new_exercise
