from operator import itemgetter
from statistics import mean

from django.test import TestCase

from exercise.factories import (
    EmailFactory,
    EmailReplyFactory,
    EmailReplyTaskScoreFactory,
    ExerciseFactory,
    ExerciseTaskFactory,
)
from participant.factories import (
    ActionLogFactory,
    ParticipantActionFactory,
    ParticipantFactory,
)


class ParticipantsTestsMixin:
    def participant_action(self, participant, action_details):
        """
        Creates a participant action.
        :param participant: OBJECT
        :param action_details: DICT (of key-value pairs to be logged as action attributes)
        :return: Action
        """
        action = ParticipantActionFactory(participant=participant)
        for key, item in action_details.items():
            ActionLogFactory(action=action, name=key, value=item)
        return action


class ParticipantModelsTests(ParticipantsTestsMixin, TestCase):
    def setUp(self):
        # tasks
        self.task_1 = ExerciseTaskFactory(
            name="Task 1",
            debrief_over_threshold="Completed Task 1!",
            debrief_under_threshold="Failed Task 1!",
            score_threshold=100,
        )
        self.task_2 = ExerciseTaskFactory(
            name="Task 2",
            debrief_over_threshold="Completed Task 2!",
            debrief_under_threshold="Failed Task 2!",
            score_threshold=75,
        )

        # email 1 with 2 replies
        self.reply_1a = EmailReplyFactory()
        self.score_1a = EmailReplyTaskScoreFactory(
            value=4, email_reply=self.reply_1a, task=self.task_1
        )
        self.reply_1b = EmailReplyFactory()
        self.score_1b = EmailReplyTaskScoreFactory(
            value=2, email_reply=self.reply_1b, task=self.task_1
        )
        self.email_1 = EmailFactory(replies=[self.reply_1a, self.reply_1b])

        # email 2 with 3 replies
        self.reply_2a = EmailReplyFactory()
        self.score_2a = EmailReplyTaskScoreFactory(
            value=1, email_reply=self.reply_2a, task=self.task_2
        )
        self.reply_2b = EmailReplyFactory()
        self.score_2b = EmailReplyTaskScoreFactory(
            value=2, email_reply=self.reply_2b, task=self.task_2
        )
        self.reply_2c = EmailReplyFactory()
        self.score_2c = EmailReplyTaskScoreFactory(
            value=3, email_reply=self.reply_2c, task=self.task_2
        )
        self.email_2 = EmailFactory(
            replies=[self.reply_2a, self.reply_2b, self.reply_2c]
        )

        # email 3 with 4 replies
        self.reply_3a = EmailReplyFactory()
        self.score_3a = EmailReplyTaskScoreFactory(
            value=1, email_reply=self.reply_3a, task=self.task_2
        )
        self.reply_3b = EmailReplyFactory()
        self.score_3b = EmailReplyTaskScoreFactory(
            value=2, email_reply=self.reply_3b, task=self.task_2
        )
        self.reply_3c = EmailReplyFactory()
        self.score_3c = EmailReplyTaskScoreFactory(
            value=3, email_reply=self.reply_3c, task=self.task_2
        )
        self.reply_3d = EmailReplyFactory()
        self.score_3d = EmailReplyTaskScoreFactory(
            value=4, email_reply=self.reply_3d, task=self.task_2
        )
        self.email_3 = EmailFactory(
            replies=[self.reply_3a, self.reply_3b, self.reply_3c, self.reply_3d]
        )

        # create the exercise
        self.exercise = ExerciseFactory(
            emails=[self.email_1, self.email_2, self.email_3]
        )

        # enroll a participant
        self.participant = ParticipantFactory(exercise=self.exercise)

    def test_participant_actions(self):
        exercise = ExerciseFactory()
        participant = ParticipantFactory(exercise=exercise)
        action_1 = self.participant_action(
            participant, {"action_type": "email_opened", "wibble": "wobble"}
        )
        action_2 = self.participant_action(
            participant, {"action_type": "random_action", "wibble": "wobble"}
        )
        expected_actions = {
            str(action_1.id): {"action_type": "email_opened", "wibble": "wobble"},
            str(action_2.id): {"action_type": "random_action", "wibble": "wobble"},
        }

        self.assertEqual(2, len(participant.actions))
        self.assertDictEqual(expected_actions, participant.actions)

    def test_participant_failed_scores(self):
        # There're no action logs recorded that can count towards these tasks,
        # hence both should be failed.
        expected_scores = [
            {
                "task": self.task_1.name,
                "score": 0,
                "debrief": self.task_1.debrief_under_threshold,
            },
            {
                "task": self.task_2.name,
                "score": 0,
                "debrief": self.task_2.debrief_under_threshold,
            },
        ]

        self.assertListEqual(expected_scores, self.participant.scores)

    def test_participant_failed_task_2(self):
        # Create an action log for sending the correct reply for an email.
        # This should mark Task 1 complete.
        self.participant_action(
            self.participant,
            {"action_type": "email_quick_reply", "reply_id": self.reply_1a.id},
        )

        expected_scores = [
            {
                "debrief": self.task_1.debrief_over_threshold,
                "score": self.score_1a.value,
                "task": self.task_1.name,
            },
            {
                "debrief": self.task_2.debrief_under_threshold,
                "score": 0,
                "task": self.task_2.name,
            },
        ]
        expected_scores = sorted(expected_scores, key=itemgetter("task"))

        self.assertListEqual(expected_scores, self.participant.scores)

    def test_participant_completed_all_tasks(self):
        # Create action logs
        # This should mark Task 1 complete.
        self.participant_action(
            self.participant,
            {
                "action_type": "email_quick_reply",
                "reply_id": self.reply_1a.id,  # scores 4
            },
        )

        # Dummy entry
        self.participant_action(
            self.participant, {"action_type": "some_event", "wibble": "wobble"}
        )

        # These events should mark Task 2 complete
        self.participant_action(
            self.participant,
            {
                "action_type": "email_quick_reply",
                "reply_id": self.reply_2b.id,  # scores 2
            },
        )
        self.participant_action(
            self.participant,
            {
                "action_type": "email_quick_reply",
                "reply_id": self.reply_3d.id,  # scores 4
            },
        )

        expected_scores = [
            {
                "debrief": self.task_1.debrief_over_threshold,
                "score": mean([self.score_1a.value]),
                "task": self.task_1.name,
            },
            {
                "debrief": self.task_2.debrief_over_threshold,
                "score": mean([self.score_2b.value, self.score_3d.value]),
                "task": self.task_2.name,
            },
        ]
        expected_scores = sorted(expected_scores, key=itemgetter("task"))

        self.assertListEqual(expected_scores, self.participant.scores)
