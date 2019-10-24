from django.db.models import Max
from .models import Exercise


def copy_exercise(original_exercise, current_user):
    """
    Create a copy of an Exercise
    :param original_exercise: An Exercise instance
    :param current_user: The user who is making a copy
    :return: Another Exercise instance copied from the original one

    """
    new_exercise = get_exercise_copy(original_exercise, current_user)
    new_exercise.initial_trial = new_exercise
    new_exercise.save()

    new_exercise.demographics.add(*original_exercise.demographics.all())
    new_exercise.emails.add(*original_exercise.emails.all())
    new_exercise.files.add(*original_exercise.files.all())

    return new_exercise


def add_trial(original_exercise, current_user):
    """
    Create a copy of an Exercise with a new trial number
    :param original_exercise: An Exercise instance
    :param current_user: The user who is making the trial
    :return: Another Exercise instance copied from the original one and added a new trial number

    """
    trial_version_count = (
        Exercise.user_objects.filter_by_user(user=current_user)
        .filter(initial_trial=original_exercise.initial_trial)
        .count()
    )

    new_exercise = get_exercise_copy(original_exercise, current_user)
    new_exercise.initial_trial = original_exercise.initial_trial
    new_exercise.trial_version = (
        trial_version_count + 1 if trial_version_count is not None else 1
    )
    new_exercise.save()

    new_exercise.demographics.add(*original_exercise.demographics.all())
    new_exercise.emails.add(*original_exercise.emails.all())
    new_exercise.files.add(*original_exercise.files.all())

    return new_exercise


def get_exercise_copy(original_exercise, current_user):

    new_exercise = Exercise(
        title=original_exercise.title + " Copy",
        description=original_exercise.description,
        introduction=original_exercise.introduction,
        afterword=original_exercise.afterword,
        length_minutes=original_exercise.length_minutes,
        training_link=original_exercise.training_link,
        debrief=original_exercise.debrief,
        copied_from=original_exercise,
        organisation=current_user.organization,
        published_by=current_user,
        updated_by=current_user,
    )

    return new_exercise
