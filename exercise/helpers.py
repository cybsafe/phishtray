from django.db.models import Q
from .models import (
    Exercise,
    ExerciseEmail,
    ExerciseEmailReply,
    EmailReplyTaskScore,
    ExerciseTask,
    ExerciseFile,
)


def copy_exercise(original_exercise, current_user):
    """
    Create a copy of an Exercise
    :param original_exercise: An Exercise instance
    :param current_user: The user who is making a copy
    :return: Another Exercise instance copied from the original one

    """
    new_exercise = get_exercise_copy(original_exercise, current_user)
    new_exercise.save()

    if original_exercise.organization == current_user.organization:
        new_exercise.demographics.add(*original_exercise.demographics.all())
        new_exercise.emails.add(*original_exercise.emails.all())
        new_exercise.files.add(*original_exercise.files.all())
    else:
        copy_emails(original_exercise, new_exercise)

    new_exercise.set_email_reveal_times()

    return new_exercise


def add_trial(original_exercise, current_user):
    """
    Create a copy of an Exercise with a new trial number
    :param original_exercise: An Exercise instance
    :param current_user: The user who is making the trial
    :return: Another Exercise instance copied from the original one and added a new trial number

    """
    initial_trial = original_exercise.initial_trial or original_exercise

    trial_version_count = (
        Exercise.user_objects.filter_by_user(user=current_user)
        .filter(Q(id=initial_trial.id) | Q(initial_trial=initial_trial))
        .count()
    )

    new_exercise = get_exercise_copy(original_exercise, current_user)

    new_exercise.initial_trial = initial_trial
    new_exercise.trial_version = trial_version_count + 1
    new_exercise.save()

    new_exercise.demographics.add(*original_exercise.demographics.all())
    new_exercise.emails.add(*original_exercise.emails.all())
    new_exercise.files.add(*original_exercise.files.all())

    new_exercise.set_email_reveal_times()

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
        copied_from=f"{original_exercise.title} - {original_exercise.id}",
        organization=current_user.organization,
        published_by=current_user,
        updated_by=current_user,
    )

    return new_exercise


def copy_email_attachment(original_file, email):
    filters = {"file_name": original_file.file_name, "organization": email.organization}

    file = ExerciseFile.objects.filter(**filters).first()

    if not file:
        file = ExerciseFile.objects.create(
            file_name=original_file.file_name,
            description=original_file.description,
            img_url=original_file.img_url,
            organization=email.organization,
        )

    return file


def copy_exercise_task_score(original_task_score, reply):
    # fetch the Task first
    filters = {
        "name": original_task_score.task.name,
        "organization": reply.organization,
    }

    task = ExerciseTask.objects.filter(**filters).first()

    if not task:
        # create a copy of the task
        task = ExerciseTask.objects.create(
            name=original_task_score.task.name,
            debrief_over_threshold=original_task_score.task.debrief_over_threshold,
            debrief_under_threshold=original_task_score.task.debrief_under_threshold,
            score_threshold=original_task_score.task.score_threshold,
            organization=reply.organization,
        )

    # Create the EmailReplyTaskScore entry for the new reply
    EmailReplyTaskScore.objects.create(
        value=original_task_score.value,
        email_reply=reply,
        task=task,
        organization=reply.organization,
    )


def copy_email_reply(original_reply, email):
    filters = {"message": original_reply.message, "organization": email.organization}

    reply = ExerciseEmailReply.objects.filter(**filters).first()

    if not reply:
        # create a copy of the original reply
        reply = ExerciseEmailReply.objects.create(
            reply_type=original_reply.reply_type,
            message=original_reply.message,
            organization=email.organization,
        )

        # copy related tasks and task scores as well
        for original_task_score in EmailReplyTaskScore.objects.filter(
            email_reply=original_reply
        ):
            copy_exercise_task_score(original_task_score, reply)

    return reply


def copy_email(original_email, new_exercise):
    filters = {
        "subject": original_email.subject,
        "organization": new_exercise.organization,
    }

    email = ExerciseEmail.objects.filter(**filters).first()

    if not email:
        # create a copy of the original email and its related data
        email = ExerciseEmail.objects.create(
            subject=original_email.subject,
            from_address=original_email.from_address,
            from_name=original_email.from_name,
            from_role=original_email.from_role,
            to_address=original_email.to_address,
            to_name=original_email.to_name,
            to_role=original_email.to_role,
            phish_type=original_email.phish_type,
            phishing_explained=original_email.phishing_explained,
            content=original_email.content,
            sort_order=original_email.sort_order,
            organization=new_exercise.organization,
        )

        # Copy Records for the ManyToMany fields
        # Replies
        replies = []
        for original_reply in original_email.replies.all():
            reply = copy_email_reply(original_reply, email)
            replies.append(reply)

        email.replies.add(*replies)

        # Attachments
        attachments = []
        for original_file in original_email.attachments.all():
            file = copy_email_attachment(original_file, email)
            attachments.append(file)

        email.attachments.add(*attachments)

        # Belongs to
        # recursively copy the one it belongs to (if it hasn't been copied already)
        if original_email.belongs_to:
            if original_email == original_email.belongs_to:
                email.belongs_to = email
            else:
                belongs_to_email = copy_email(original_email.belongs_to, new_exercise)
                email.belongs_to = belongs_to_email
            email.save()

    return email


def copy_emails(original_exercise, new_exercise):
    emails = []
    for original_email in original_exercise.emails.all():
        email = copy_email(original_email, new_exercise)
        emails.append(email)

    new_exercise.emails.add(*emails)
