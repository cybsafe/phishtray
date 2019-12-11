from django.db import transaction
from django.db.models import Q
from .models import (
    Exercise,
    ExerciseEmail,
    ExerciseEmailReply,
    EmailReplyTaskScore,
    ExerciseTask,
    ExerciseFile,
    ExerciseEmailProperties,
    ExerciseWebPage,
    ExerciseWebPageReleaseCode,
    DemographicsInfo,
)


def copy_exercise(original_exercise, current_user):
    """
    Create a copy of an Exercise
    :param original_exercise: An Exercise instance
    :param current_user: The user who is making a copy
    :return: Another Exercise instance copied from the original one

    """
    with transaction.atomic():
        new_exercise = get_exercise_copy(original_exercise, current_user)
        new_exercise.save()
        copy_demographics_info(original_exercise, new_exercise)
        copy_files(original_exercise, new_exercise)
        copy_emails(original_exercise, new_exercise)
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

    with transaction.atomic():
        new_exercise = get_exercise_copy(original_exercise, current_user)

        new_exercise.initial_trial = initial_trial
        new_exercise.trial_version = trial_version_count + 1
        new_exercise.save()

        copy_demographics_info(original_exercise, new_exercise)
        copy_files(original_exercise, new_exercise)
        copy_emails(original_exercise, new_exercise)

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


def copy_demographics_info(original_exercise, new_exercise):
    demographics = []
    for original_demographics in original_exercise.demographics.all():
        filters = {
            "question": original_demographics.question,
            "organization": new_exercise.organization,
        }
        demo_info = DemographicsInfo.objects.filter(**filters).first()
        if not demo_info:
            demo_info = DemographicsInfo.objects.create(
                question_type=original_demographics.question_type,
                question=original_demographics.question,
                required=original_demographics.required,
                organization=new_exercise.organization,
            )
        demographics.append(demo_info)

    new_exercise.demographics.add(*demographics)


def copy_file(original_file, obj):
    """
    Copies a file to the obj's organization (unless it's already avail there).
    :param original_file:
    :param obj: an instance with organization attribute - this will be used to determine the new file's organisation
    :return: ExerciseFile instance
    """
    filters = {"file_name": original_file.file_name, "organization": obj.organization}
    file = ExerciseFile.objects.filter(**filters).first()
    if not file:
        file = ExerciseFile.objects.create(
            file_name=original_file.file_name,
            description=original_file.description,
            img_url=original_file.img_url,
            organization=obj.organization,
        )
    return file


def copy_files(original_exercise, new_exercise):
    files = []
    for original_file in original_exercise.files.all():
        file = copy_file(original_file, new_exercise)
        files.append(file)

    new_exercise.files.add(*files)


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
        "sort_order": original_email.sort_order,
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
            file = copy_file(original_file, email)
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


def copy_webpage(original_webpage, new_exercise):
    if original_webpage is None:
        return None

    filters = {"url": original_webpage.url, "organization": new_exercise.organization}

    webpage = ExerciseWebPage.objects.filter(**filters).first()

    if not webpage:
        webpage = ExerciseWebPage.objects.create(
            title=original_webpage.title,
            url=original_webpage.url,
            type=original_webpage.type,
            content=original_webpage.content,
            organization=new_exercise.organization,
        )

    return webpage


def copy_webpage_release_codes(original_release_code, new_exercise):
    filters = {
        "release_code": original_release_code.release_code,
        "organization": new_exercise.organization,
    }

    release_code = ExerciseWebPageReleaseCode.objects.filter(**filters).first()

    if not release_code:
        release_code = ExerciseWebPageReleaseCode.objects.create(
            release_code=original_release_code.release_code,
            organization=new_exercise.organization,
        )

    return release_code


def copy_email_properties(
    original_email, original_exercise, target_email, target_exercise
):
    """
    Copies email properties from the original exercise to target.
    """
    original_email_props = ExerciseEmailProperties.objects.get(
        exercise_id=original_exercise.id, email_id=original_email.id
    )
    webpage = copy_webpage(original_email_props.web_page, target_exercise)
    email_props = ExerciseEmailProperties.objects.create(
        exercise=target_exercise,
        email=target_email,
        reveal_time=original_email_props.reveal_time,
        web_page=webpage,
        intercept_exercise=original_email_props.intercept_exercise,
        date_received=original_email_props.date_received,
    )

    # Add release codes
    codes = []
    for release_code in original_email_props.release_codes.all():
        code = copy_webpage_release_codes(release_code, target_exercise)
        codes.append(code)

    email_props.release_codes.add(*codes)


def copy_emails(original_exercise, new_exercise):
    emails = []
    for original_email in original_exercise.emails.all():
        email = copy_email(original_email, new_exercise)
        emails.append(email)
        copy_email_properties(original_email, original_exercise, email, new_exercise)

    new_exercise.emails.add(*emails)
