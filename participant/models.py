from operator import itemgetter
from statistics import mean

from participant.constants import (
    ParticipantBehaviour,
    POSITIVE_ACTIONS,
    NEGATIVE_ACTIONS,
)
from .managers import ParticipantManager, OrganizationManager

from django.db import models
from exercise.models import (
    DemographicsInfo,
    Exercise,
    ExerciseEmail,
    ExerciseFile,
    ExerciseEmailReply,
    ExerciseTask,
)

from phishtray.base import PhishtrayBaseModel

STARTED_EXPERIMENT = 0
COMPLETED_EXPERIMENT = 1
OPENED_EMAIL = 2
OPENED_UNSAFE_EMAIL_LINK = 3
DOWNLOADED_UNSAFE_EMAIL_ATTACHMENT = 4

EVENT_TYPES = (
    (STARTED_EXPERIMENT, "started"),
    (COMPLETED_EXPERIMENT, "completed"),
    (OPENED_EMAIL, "opened"),
    (OPENED_UNSAFE_EMAIL_LINK, "unsafe_link"),
    (DOWNLOADED_UNSAFE_EMAIL_ATTACHMENT, "unsafe_attachment"),
)


class ParticipantProfileEntry(PhishtrayBaseModel):
    """
    Aggregates Demographic Info
    """

    demographics_info = models.ForeignKey(DemographicsInfo, on_delete=models.PROTECT)
    answer = models.CharField(max_length=180, blank=True, null=True)

    @property
    def question(self):
        return self.demographics_info.question

    def __str__(self):
        return "{} - {}".format(self.question, self.answer)


class Participant(PhishtrayBaseModel):
    def __str__(self):
        return "Participant: {} For: {}".format(self.id, self.exercise)

    objects = ParticipantManager()

    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    profile = models.ManyToManyField(ParticipantProfileEntry)
    organization = models.ForeignKey(
        "participant.Organization", null=True, blank=True, on_delete=models.DO_NOTHING
    )

    @property
    def actions(self):
        """

        :return: DICT
        """
        actions = {}
        entries = ActionLog.objects.filter(action__participant=self).order_by(
            "created_date"
        )

        for entry in entries:
            action_details = actions.setdefault(str(entry.action_id), {})
            action_details.setdefault(entry.name, entry.value)

        return actions

    def phishing_email_behaviour_and_actions(self, email_id):
        """
        Aggregates actions related to a phishing email and determines behaviour.

        :param email_id: UUID - id of an email
        :return: (DICT, LIST) - returns a tuple of participant behaviour and actions
        """

        def participant_behaviour(actions):
            behaviour = ParticipantBehaviour.NEUTRAL
            action_id = None

            for action in actions:
                if action.get("action_type") in POSITIVE_ACTIONS:
                    behaviour = ParticipantBehaviour.POSITIVE
                    action_id = action.get("action_id")

                if action.get("action_type") in NEGATIVE_ACTIONS:
                    behaviour = ParticipantBehaviour.NEGATIVE
                    action_id = action.get("action_id")
                    break

            pb = {"behaviour": behaviour, "action_id": action_id}
            return pb

        actions = []

        if email_id in self.exercise.phishing_email_ids:
            for action_id, action_details in self.actions.items():
                if email_id == action_details.get("email_id"):
                    action_details["action_id"] = action_id
                    actions.append(action_details)

        return participant_behaviour(actions), actions

    @property
    def pid(self):
        """
        Returns Prolific ID or None
        """
        entry = self.profile.filter(
            demographics_info__question__icontains="prolific id"
        ).first()
        if entry:
            return entry.answer
        else:
            return None

    @property
    def scores(self):
        exercise_replies = ExerciseEmailReply.objects.filter(
            exerciseemail__in=self.exercise.emails.all()
        ).distinct()

        scores = []
        tasks = {}

        # 1. Add defaults to `task` for each linked task:
        #   DICT:
        #       task_id: 0
        for reply in exercise_replies:
            for reply_score in reply.scores:
                task = reply_score.task
                tasks.setdefault(str(task.id), [])

        if not tasks:
            return scores

        # 2. collect actions where action_type is `email_quick_reply`
        # and a `reply_id` is present

        reply_actions = []
        for action_id, action_details in self.actions.items():
            if (
                "reply_id" in action_details
                and action_details.get("action_type") == "email_quick_reply"
            ):
                # The participant has sent a respone so let's add
                reply_actions.append(self.actions[action_id])

        # 3. Update recorded scores based on participant actions

        for action in reply_actions:
            email_reply = exercise_replies.filter(id=action["reply_id"])
            if email_reply:
                for reply_score in email_reply.first().scores:
                    score = reply_score.value
                    task = reply_score.task
                    tasks[str(task.id)].append(score)

        # 4. prepare the response by looping through the previous dict we prepared
        # returning the name of the task, the score and debrief which gets picked by score evaluation

        # pre-fetch all tasks that belong to the exercise
        exercise_tasks = ExerciseTask.objects.filter(
            emailreplytaskscore__email_reply__in=exercise_replies
        ).distinct()

        for task_id, score_data in tasks.items():
            task = exercise_tasks.get(id=task_id)
            score = mean(score_data or [0])
            scores.append(
                {"task": task.name, "score": score, "debrief": task.evaluate(score)}
            )

        return sorted(scores, key=itemgetter("task"))


class ParticipantAction(PhishtrayBaseModel):
    """
    Groups a set of ActionLogs together.
    """

    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)


class ActionLog(PhishtrayBaseModel):
    """
    Simple key/value entries representing Participant actions.
    """

    action = models.ForeignKey(ParticipantAction, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, null=False)
    value = models.CharField(max_length=2000, blank=False, null=False)


class Organization(models.Model):
    """
    Organization Model.
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    objects = OrganizationManager()
