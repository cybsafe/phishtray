from operator import itemgetter
from statistics import mean

from django.db import models
from exercise.models import (
    DemographicsInfo,
    Exercise,
    ExerciseEmail,
    ExerciseFile,
    ExerciseEmailReply,
    ExerciseTask
)

from phishtray.base import PhishtrayBaseModel

STARTED_EXPERIMENT = 0
COMPLETED_EXPERIMENT = 1
OPENED_EMAIL = 2
OPENED_UNSAFE_EMAIL_LINK = 3
DOWNLOADED_UNSAFE_EMAIL_ATTACHMENT = 4

EVENT_TYPES = (
    (STARTED_EXPERIMENT, 'started'),
    (COMPLETED_EXPERIMENT, 'completed'),
    (OPENED_EMAIL, 'opened'),
    (OPENED_UNSAFE_EMAIL_LINK, 'unsafe_link'),
    (DOWNLOADED_UNSAFE_EMAIL_ATTACHMENT, 'unsafe_attachment'),
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
        return '{} - {}'.format(self.question, self.answer)


class Participant(PhishtrayBaseModel):

    def __str__(self):
        return 'Participant: {} For: {}'.format(self.id, self.exercise)

    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
    profile = models.ManyToManyField(ParticipantProfileEntry)

    @property
    def actions(self):
        """

        :return: DICT
        """
        actions = {}
        entries = ActionLog.objects.filter(
            action__participant=self).order_by('created_date')

        for entry in entries:
            action_details = actions.setdefault(str(entry.action_id), {})
            action_details.setdefault(entry.name, entry.value)

        return actions


    @property
    def scores(self):
        exercise_replies = ExerciseEmailReply.objects.filter(
            exerciseemail__in=self.exercise.emails.all()).distinct()

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
            if ('reply_id' in action_details and
                    action_details.get('action_type') == 'email_quick_reply'):
                # The participant has sent a respone so let's add
                reply_actions.append(self.actions[action_id])

        # 3. Update recorded scores based on participant actions

        for action in reply_actions:
            email_reply = exercise_replies.filter(id=action['reply_id'])
            if email_reply:
                for reply_score in email_reply.first().scores:
                    score = reply_score.value
                    task = reply_score.task
                    tasks[str(task.id)].append(score)

        # 4. prepare the response by looping through the previous dict we prepared
        # returning the name of the task, the score and debrief which gets picked by score evaluation

        # pre-fetch all tasks that belong to the exercise
        exercise_tasks = ExerciseTask.objects.filter(
            emailreplytaskscore__email_reply__in=exercise_replies).distinct()

        for task_id, score_data in tasks.items():
            task = exercise_tasks.get(id=task_id)
            score = mean(score_data or [0])
            scores.append({
                'task': task.name,
                'score': score,
                'debrief': task.evaluate(score)
            })

        return sorted(scores, key=itemgetter('task'))


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
