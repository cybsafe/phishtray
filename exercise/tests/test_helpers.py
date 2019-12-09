from django.test import TestCase

from phishtray.test.base import ThreadTestsMixin
from ..factories import (
    ExerciseFactory,
    EmailFactory,
    EmailReplyFactory,
    ExerciseTaskFactory,
    EmailReplyTaskScoreFactory,
    ExerciseFileFactory,
    ExerciseWebPageFactory,
    ExerciseWebPageReleaseCodeFactory,
    DemographicsInfoFactory,
)
from ..models import (
    Exercise,
    ExerciseEmail,
    ExerciseEmailReply,
    EmailReplyTaskScore,
    ExerciseTask,
    ExerciseFile,
    ExerciseWebPage,
    ExerciseWebPageReleaseCode,
    DemographicsInfo,
)
from ..helpers import copy_exercise, add_trial

from participant.factories import OrganizationFactory
from users.factories import UserFactory


class ExerciseHelperTests(ThreadTestsMixin, TestCase):
    def setUp(self):
        self.organization = OrganizationFactory()
        self.user = UserFactory(
            username="user_with_organization", organization=self.organization
        )

    def test_copy_exercise(self):
        """
        Testing helper method that copies an exercise
        """
        exercise = ExerciseFactory()

        copied_exercise = copy_exercise(exercise, self.user)

        self.assertIsNotNone(copied_exercise)
        self.assertEqual(exercise, copied_exercise.copied_from_exercise)
        self.assertEqual(1, copied_exercise.trial_version)
        self.assertIsNone(copied_exercise.initial_trial)
        self.assertEqual(2, Exercise.objects.all().count())

        self.assertEqual(
            exercise.demographics.all().count(),
            copied_exercise.demographics.all().count(),
        )
        self.assertEqual(
            exercise.emails.all().count(), copied_exercise.emails.all().count()
        )
        self.assertEqual(
            exercise.files.all().count(), copied_exercise.files.all().count()
        )

        self.assertEqual(1, Exercise.objects.filter(copied_from=exercise).count())

    def test_copy_exercise_copies_emails_and_associated_records(self):
        """
        When copying an exercise it should also copy the linked emails.
        These copies should be bound to the user's organisation,
        if those were not available before.
        (** Availability is judged on the subject field)
        """
        email_count = 2
        emails = EmailFactory.create_batch(email_count)
        exercise = ExerciseFactory.create(emails=emails)

        qs = ExerciseEmail.objects.filter_by_org_private(self.user)

        # The Organisation should have no emails at this stage
        self.assertFalse(qs.count(), "Unexpected emails in organisation!")

        copied_exercise = copy_exercise(exercise, self.user)

        self.assertEquals(email_count, qs.count())

        # All emails should've been copied,
        # so the copied exercise shouldn't use any of the old emails
        self.assertFalse(
            set([e.id for e in emails]) & set(qs.values_list("id")),
            "Unexpected email found in the copied exercise.",
        )

    def test_copy_email_copies_associated_replies(self):
        """
        When an email is copied it should also copy the related email replies.
        # When an email is copied it should also copy the associated records (tasks, scores, files).
        # These copies should be bound to the user's organisation, if those were not available before.
        # (** Availability is judged on fields message, name, file_name respectively)
        """
        # Prep Org items
        org_reply_01 = EmailReplyFactory(
            message="wobble", organization=self.organization
        )

        # Prep Public Exercise
        reply_01 = EmailReplyFactory()
        reply_02 = EmailReplyFactory(message="wobble")
        public_replies = [reply_01, reply_02]
        email = EmailFactory()
        email.replies.add(*public_replies)
        exercise = ExerciseFactory.create(emails=[email])

        qs = ExerciseEmailReply.objects.filter_by_org_private(self.user)

        self.assertEquals(1, qs.count(), "Unexpected email replies in organisation!")

        copied_exercise = copy_exercise(exercise, self.user)

        self.assertEquals(2, qs.count())
        copied_email = copied_exercise.emails.first()
        # None of the replies linked to the public exercise's email should be linked
        self.assertFalse(
            set([e.id for e in public_replies])
            & set(copied_email.replies.values_list("id")),
            "Unexpected email reply found in the copied email.",
        )
        # reply_02 matches with org_reply_01 so it was not copied
        # instead org_reply_01 will get assiciated with the new email that was made avail to the org
        self.assertTrue(org_reply_01 in copied_email.replies.all())

    def test_copy_email_reply_copies_associated_tasks_and_scores(self):
        """
        When an email reply is copied it should also copy the related tasks and scores.
        It should create the task if it was not available in the organisation before.
        """
        task = ExerciseTaskFactory(
            name="Task 1",
            debrief_over_threshold="Completed Task 1!",
            debrief_under_threshold="Failed Task 1!",
            score_threshold=100,
        )
        reply = EmailReplyFactory()
        score = 3
        EmailReplyTaskScoreFactory(value=score, email_reply=reply, task=task)
        email = EmailFactory()
        email.replies.add(*[reply])
        exercise = ExerciseFactory.create(emails=[email])

        task_qs = ExerciseTask.objects.filter_by_org_private(self.user)
        scores_qs = EmailReplyTaskScore.objects.filter_by_org_private(self.user)

        self.assertFalse(task_qs.count(), "Unexpected tasks in organisation!")
        self.assertFalse(scores_qs.count(), "Unexpected tasks scores in organisation!")

        copied_exercise = copy_exercise(exercise, self.user)

        self.assertEquals(1, task_qs.count())
        self.assertEquals(1, scores_qs.count())
        self.assertEquals(score, scores_qs.first().value)

        # Copies are expected instead of transfer of ownership
        self.assertFalse(
            {task.id, reply.id}
            & {task_qs.values_list("id"), scores_qs.first().email_reply.id}
        )

    def test_copy_email_reply_use_existing_task_and_creates_new_task_score(self):
        """
        When an email reply is copied it should also copy the related tasks and scores.
        However, if a task is already available in the target organisation that task
        should be associated with the copied email reply and a new task score should be created.
        """
        org_task = ExerciseTaskFactory(
            name="Task 1",
            debrief_over_threshold="Completed Task 1!",
            debrief_under_threshold="Failed Task 1!",
            score_threshold=100,
            organization=self.organization,
        )
        task = ExerciseTaskFactory(
            name="Task 1",
            debrief_over_threshold="Completed Task 1!",
            debrief_under_threshold="Failed Task 1!",
            score_threshold=100,
        )
        reply = EmailReplyFactory()
        score = 3
        EmailReplyTaskScoreFactory(value=score, email_reply=reply, task=task)
        email = EmailFactory()
        email.replies.add(*[reply])
        exercise = ExerciseFactory.create(emails=[email])

        task_qs = ExerciseTask.objects.filter_by_org_private(self.user)
        scores_qs = EmailReplyTaskScore.objects.filter_by_org_private(self.user)

        self.assertEquals(1, task_qs.count(), "Unexpected tasks in organisation!")
        self.assertFalse(scores_qs.count(), "Unexpected tasks scores in organisation!")

        copied_exercise = copy_exercise(exercise, self.user)

        self.assertEquals(1, task_qs.count())
        self.assertEquals(1, scores_qs.count())
        self.assertEquals(score, scores_qs.first().value)
        self.assertEquals(org_task, scores_qs.first().task)

        # Copies are expected instead of transfer of ownership
        self.assertNotEquals(reply.id, scores_qs.first().email_reply.id)

    def test_copy_email_copies_email_attachments(self):
        # Prep Org items
        org_file_01 = ExerciseFileFactory(
            file_name="wibble.pdf", organization=self.organization
        )

        # Prep Public Exercise
        file_01 = ExerciseFileFactory()
        file_02 = ExerciseFileFactory(file_name="wibble.pdf")
        public_files = [file_01, file_02]
        email = EmailFactory()
        email.attachments.add(*public_files)
        exercise = ExerciseFactory.create(emails=[email])

        qs = ExerciseFile.objects.filter_by_org_private(self.user)

        self.assertEquals(1, qs.count(), "Unexpected files in organisation!")

        copied_exercise = copy_exercise(exercise, self.user)

        self.assertEquals(2, qs.count())
        copied_email = copied_exercise.emails.first()
        self.assertEquals(2, copied_email.attachments.count())
        # None of the files linked to the public exercise's email should be listed as an attachment
        self.assertFalse(
            set([e.id for e in public_files])
            & set(copied_email.attachments.values_list("id")),
            "Unexpected attachments found in the copied email.",
        )
        # file_02 matches with org_file_01 so it was not copied
        # instead org_file_01 will get associated with the new email that was made avail to the org
        self.assertTrue(org_file_01 in copied_email.attachments.all())

    def test_copy_email_deep_copies_belongs_to(self):
        """
        Emails that are the head of the thread `belongs_to` themselves.
        Emails that are part of a thread chain `belongs_to` other emails.
        If an email is being copied that's not a head of the thread
        it would need the head (email) to be copied prior to populating its `belongs_to` field.
        Note: The order of which the emails get copied is random.
        """
        emails = EmailFactory.create_batch(2)
        thread_subject = "X-Men cinema tickets 4 FREE!"
        thread_head = EmailFactory(subject=thread_subject)
        self.threadify(thread_head)
        emails.append(thread_head)
        self.threadify(emails[0], thread_head)
        self.threadify(emails[1], thread_head)
        exercise = ExerciseFactory.create(emails=emails)

        qs = ExerciseEmail.objects.filter_by_org_private(self.user)
        self.assertEquals(0, qs.count())

        copied_exercise = copy_exercise(exercise, self.user)

        # After copying the exercise the organisation will have 3 emails that all belong to the same thread.
        qs = ExerciseEmail.objects.filter_by_org_private(self.user)
        self.assertEquals(3, qs.filter(belongs_to__subject=thread_subject).count())

    def test_copy_email_properties(self):
        """
        When copying an exercise, related emails with the relevant email properties should be copied as well.
        Webpages and release codes should also be copied if they are linked to the given email properties.
        :return:
        """
        webpage = ExerciseWebPageFactory()
        release_code = ExerciseWebPageReleaseCodeFactory()
        email = EmailFactory()
        exercise = ExerciseFactory.create(emails=[email])
        exercise.sync_email_properties()

        # Add some data to email properties
        props = email.exercise_specific_properties(exercise)
        props.reveal_time = 60
        props.web_page = webpage
        props.release_codes.add(release_code)
        props.save()

        webpage_qs = ExerciseWebPage.objects.filter_by_org_private(self.user)
        release_code_qs = ExerciseWebPageReleaseCode.objects.filter_by_org_private(
            self.user
        )

        self.assertEquals(0, webpage_qs.count())
        self.assertEquals(0, release_code_qs.count())

        copied_exercise = copy_exercise(exercise, self.user)

        self.assertEquals(1, webpage_qs.count())
        self.assertEquals(1, release_code_qs.count())

        # Email Properties
        copied_email = copied_exercise.emails.first()
        copied_props = copied_email.exercise_specific_properties(copied_exercise)
        self.assertNotEquals(props.id, copied_props.id)
        self.assertNotEquals(props.email, copied_props.email)
        self.assertNotEquals(props.exercise, copied_props.exercise)
        self.assertEquals(props.reveal_time, copied_props.reveal_time)

        # Web page
        self.assertNotEquals(props.web_page, copied_props.web_page)
        self.assertEquals(props.web_page.title, copied_props.web_page.title)

        # Release codes
        self.assertNotEquals(
            props.release_codes.first().id, copied_props.release_codes.first().id
        )
        self.assertEquals(
            props.release_codes.first().release_code,
            copied_props.release_codes.first().release_code,
        )

    def test_copy_public_exercise_copies_demographics_info(self):
        """
        When a public exercise is copied, demographics should be copied to the user's organization.
        """
        di = DemographicsInfoFactory()
        exercise = ExerciseFactory()
        exercise.demographics.add(di)

        qs = DemographicsInfo.objects.filter_by_org_private(self.user)
        self.assertEquals(0, qs.count())

        copied_exercise = copy_exercise(exercise, self.user)

        self.assertEquals(1, qs.count())
        copied_di = copied_exercise.demographics.first()
        self.assertNotEquals(di.id, copied_di.id)
        self.assertEquals(di.question, copied_di.question)
        self.assertEquals(di.question_type, copied_di.question_type)

    def test_copy_exercise_adds_demographics_info(self):
        """
        When exercise is copied within an organisation, demographics should not be duplicated.
        """
        di = DemographicsInfoFactory(organization=self.organization)
        exercise = ExerciseFactory(organization=self.organization)
        exercise.demographics.add(di)

        qs = DemographicsInfo.objects.filter_by_org_private(self.user)
        self.assertEquals(1, qs.count())

        copied_exercise = copy_exercise(exercise, self.user)

        self.assertEquals(1, qs.count())
        copied_di = copied_exercise.demographics.first()
        self.assertEquals(di.id, copied_di.id)
        self.assertEquals(di.question, copied_di.question)
        self.assertEquals(di.question_type, copied_di.question_type)

    def test_copy_public_exercise_copies_exercise_files(self):
        """
        When a public exercise is copied, files should be copied to the user's organization.
        """
        file = ExerciseFileFactory()
        exercise = ExerciseFactory()
        exercise.files.add(file)

        qs = ExerciseFile.objects.filter_by_org_private(self.user)
        self.assertEquals(0, qs.count())

        copied_exercise = copy_exercise(exercise, self.user)

        self.assertEquals(1, qs.count())
        copied_file = copied_exercise.files.first()
        self.assertNotEquals(file.id, copied_file.id)
        self.assertEquals(file.file_name, copied_file.file_name)

    def test_copy_exercise_adds_exercise_files(self):
        """
        When exercise is copied within an organisation, files should not be duplicated.
        """
        file = ExerciseFileFactory(organization=self.organization)
        exercise = ExerciseFactory(organization=self.organization)
        exercise.files.add(file)

        qs = ExerciseFile.objects.filter_by_org_private(self.user)
        self.assertEquals(1, qs.count())

        copied_exercise = copy_exercise(exercise, self.user)

        self.assertEquals(1, qs.count())
        copied_file = copied_exercise.files.first()
        self.assertEquals(file.id, copied_file.id)
        self.assertEquals(file.file_name, copied_file.file_name)

    def test_trial_exercise(self):
        """
        Testing helper method that make a trial of an exercise
        """
        exercise = ExerciseFactory(organization=self.organization)
        trial_exercise = add_trial(exercise, self.user)

        self.assertIsNotNone(trial_exercise)
        self.assertEqual(2, Exercise.objects.all().count())

        self.assertEqual(exercise, trial_exercise.copied_from_exercise)
        self.assertEqual(exercise, trial_exercise.initial_trial)

        self.assertEqual(2, trial_exercise.trial_version)

        self.assertEqual(
            exercise.demographics.all().count(),
            trial_exercise.demographics.all().count(),
        )
        self.assertEqual(
            exercise.emails.all().count(), trial_exercise.emails.all().count()
        )
        self.assertEqual(
            exercise.files.all().count(), trial_exercise.files.all().count()
        )

        self.assertEqual(1, Exercise.objects.filter(copied_from=exercise).count())

    def test_trial_exercises(self):
        """
        Testing helper method that make trials of an exercise
        """
        exercise = ExerciseFactory(organization=self.organization)
        trial_exercise = add_trial(exercise, self.user)
        another_trial_exercise = add_trial(exercise, self.user)

        self.assertIsNotNone(trial_exercise)
        self.assertIsNotNone(another_trial_exercise)
        self.assertEqual(3, Exercise.objects.all().count())

        self.assertEqual(exercise, trial_exercise.copied_from_exercise)
        self.assertEqual(exercise, another_trial_exercise.copied_from_exercise)

        self.assertEqual(exercise, trial_exercise.initial_trial)
        self.assertEqual(exercise, another_trial_exercise.initial_trial)

        self.assertEqual(2, trial_exercise.trial_version)
        self.assertEqual(3, another_trial_exercise.trial_version)

        self.assertEqual(2, Exercise.objects.filter(copied_from=exercise).count())
        self.assertEqual(2, Exercise.objects.filter(initial_trial=exercise).count())
