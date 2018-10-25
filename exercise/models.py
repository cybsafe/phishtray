from math import ceil, floor
from random import randrange, random

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from phishtray.base import PhishtrayBaseModel


EXERCISE_EMAIL_PHISH = 0
EXERCISE_EMAIL_REGULAR = 1
EXERCISE_EMAIL_ETRAY = 2

EXERCISE_PHISH_TYPES = (
    (EXERCISE_EMAIL_PHISH, 'phishing'),
    (EXERCISE_EMAIL_REGULAR, 'regular'),
    (EXERCISE_EMAIL_ETRAY, 'etray'),
)

EXERCISE_REPLY_TYPE = (
    (0, 'reply'),
    (1, 'forward')
)


class ExerciseTask(PhishtrayBaseModel):
    """
    Tasks are a way to define a metric for scoring in the psychometric evaluation
    """
    name = models.CharField(max_length=250, blank=True, null=True)
    debrief_over_threshold = models.TextField(null=True, blank=True)
    debrief_under_threshold = models.TextField(null=True, blank=True)
    score_threshold = models.IntegerField()

    def evaluate(self, score):
        """
        Constraints:
            1. Scores should only range from 1 to 4.
            2. Tasks should be unique in an exercise.
            2. Tasks should not be shared between exercises.
            3. Threshold is set percentage based with range 1-100.
        :param score: INT / FLOAT
            - this is calculated from a list of numbers with mean()
        :return: STRING
        """
        scores = EmailReplyTaskScore.objects.filter(task=self)
        acceptance_threshold = 4 * (self.score_threshold / 100)
        if score >= acceptance_threshold:
            return self.debrief_over_threshold
        else:
            return self.debrief_under_threshold

    def __str__(self):
        return self.name


class ExerciseFile(PhishtrayBaseModel):
    """
    ExercieseFiles are not actual files but they act like one.
    """
    file_name = models.CharField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    # img_url - used for file representation (e.g.: screenshot of the file)
    # Provide default image?
    img_url = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.file_name


class ExerciseEmailReply(PhishtrayBaseModel):
    reply_type = models.IntegerField(choices=EXERCISE_REPLY_TYPE, null=True)
    message = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Exercise email replies "

    @property
    def scores(self):
        """
        EmailReplies can carry Tasks with a corresponding score.
        This is irrespective of which exercise and emailreply is used.
        """
        return EmailReplyTaskScore.objects.all().filter(email_reply=self)

    def __str__(self):
        return self.message


class EmailReplyTaskScore(PhishtrayBaseModel):
    """
    A method to associate scores to email replies.
    """

    value = models.IntegerField()
    email_reply = models.ForeignKey(
        ExerciseEmailReply, on_delete=models.CASCADE, null=True, blank=True)
    task = models.ForeignKey(ExerciseTask, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "Reply: {self.email_reply} - {self.task} - {self.value}".format(self=self)


class ExerciseEmail(PhishtrayBaseModel):

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['sort_order']

    subject = models.CharField(max_length=250, blank=True, null=True)

    # TODO: introduce new model i.e.: Account to store these info
    from_address = models.CharField(max_length=250, blank=True, null=True)
    from_name = models.CharField(max_length=250, blank=True, null=True)
    from_profile_img_url = models.CharField(max_length=150, blank=True, null=True)
    from_role = models.CharField(max_length=50, blank=True, null=True)

    # TODO: introduce new model i.e.: Account to store these info
    to_address = models.CharField(max_length=250, blank=True, null=True)
    to_name = models.CharField(max_length=250, blank=True, null=True)
    to_profile_img_url = models.CharField(max_length=150, blank=True, null=True)
    to_role = models.CharField(max_length=50, blank=True, null=True)

    phish_type = models.IntegerField(choices=EXERCISE_PHISH_TYPES)
    content = models.TextField(null=True, blank=True)
    attachments = models.ManyToManyField(ExerciseFile, blank=True)
    replies = models.ManyToManyField(ExerciseEmailReply, blank=True)
    belongs_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    sort_order = models.IntegerField(default=0)

    @property
    def from_account(self):
        data = {
            'email': self.from_address,
            'name': self.from_name,
            'photo_url': self.from_profile_img_url,
            'role': self.from_role,
        }
        return data

    @property
    def to_account(self):
        data = {
            'email': self.to_address,
            'name': self.to_name,
            'photo_url': self.to_profile_img_url,
            'role': self.to_role,
        }
        return data

    @property
    def reveal_time(self):
        email = ExerciseEmailProperties.objects.filter(
            email_id=self.id, exercise__emails__id=self.id).first()
        if email:
            return email.reveal_time


class DemographicsInfo(PhishtrayBaseModel):
    """
    Demographic Questions that can be added to Exercises.
    """
    QUESTION_TYPE_INTEGER = 0
    QUESTION_TYPE_TEXT = 1

    QUESTION_TYPES = (
        (QUESTION_TYPE_INTEGER, 'number'),
        (QUESTION_TYPE_TEXT, 'string'),
    )

    question_type = models.IntegerField(choices=QUESTION_TYPES)
    question = models.CharField(max_length=180, blank=True, null=True)
    required = models.BooleanField(
        help_text='Mark question mandatory on the participant form.',
        default=False
    )

    def __str__(self):
        return self.question


class Exercise(PhishtrayBaseModel):

    def __str__(self):
        return self.title

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    introduction = models.TextField(null=True, blank=True)
    afterword = models.TextField(null=True, blank=True)
    length_minutes = models.IntegerField()
    demographics = models.ManyToManyField(DemographicsInfo, blank=True)
    emails = models.ManyToManyField(ExerciseEmail, blank=True)
    files = models.ManyToManyField(ExerciseFile, blank=True)

    def set_email_reveal_times(self):
        emails = list(self.emails.all())
        if not emails:
            return

        # Set some emails based on a threshold to zero time initially.
        received_emails_count = int(ceil((len(emails) * settings.REVEAL_TIME_ZERO_THRESHOLD)))

        while received_emails_count > 0:
            email = emails.pop(randrange(len(emails)))
            email_properties = ExerciseEmailProperties.objects.filter(
                exercise_id=self.id, email_id=email.id
            ).first()
            if email_properties:
                email_properties.set_reveal_time(0)
            received_emails_count -= 1

        # Remaining emails without a set time to be set to a random time
        for email in emails:
            # This creates a random distribution that tends to drift towards the beginning of the exercise.
            rand_time = int(floor(abs(random() - random()) * (1 + self.length_minutes * 60)))
            ExerciseEmailProperties.objects.get(
                exercise_id=self.id, email_id=email.id).set_reveal_time(rand_time)


class ExerciseEmailProperties(PhishtrayBaseModel):

    class Meta:
        unique_together = ('exercise', 'email',)

    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE,)
    email = models.ForeignKey(ExerciseEmail, on_delete=models.CASCADE,)
    reveal_time = models.PositiveIntegerField(blank=True, null=True, help_text="Time in seconds.",)

    def set_reveal_time(self, time):
        if self.reveal_time is None:
            self.reveal_time = time
            self.save()


class ExerciseWebPages(PhishtrayBaseModel):

    def __str__(self):
        return self.subject

    subject = models.CharField(max_length=250, blank=True, null=True)
    url = models.CharField(max_length=250, blank=True, null=True)
    type = models.IntegerField(choices=EXERCISE_PHISH_TYPES)
    content = models.TextField(null=True, blank=True)


class ExerciseURL(PhishtrayBaseModel):

    def __str__(self):
        return self.subject

    subject = models.CharField(max_length=250, blank=True, null=True)
    actual_url = models.CharField(max_length=250, blank=True, null=True)
    real_url = models.CharField(max_length=250, blank=True, null=True)
    type = models.IntegerField(choices=EXERCISE_PHISH_TYPES)

    web_page = models.ForeignKey(ExerciseWebPages, on_delete=models.CASCADE)


@receiver(post_save, sender=Exercise)
def create_email_reveal_time(sender, instance, created, **kwargs):
    """Create email reveal times when an exercise email instance is created."""
    for email in ExerciseEmail.objects.reverse():
        ExerciseEmailProperties.objects.get_or_create(exercise_id=instance.id, email_id=email.id)

    # Set the email reveal times
    instance.set_email_reveal_times()
