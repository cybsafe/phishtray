from math import ceil, floor
from random import randrange, random

from django.conf import settings
from django.db import models

from phishtray.base import PhishtrayBaseModel, MultiTenantMixin
from .managers import ExerciseManager, ExerciseEmailPropertiesManager


EXERCISE_EMAIL_PHISH = 0
EXERCISE_EMAIL_REGULAR = 1

EXERCISE_PHISH_TYPES = (
    (EXERCISE_EMAIL_PHISH, "phishing"),
    (EXERCISE_EMAIL_REGULAR, "regular"),
)

EXERCISE_REPLY_TYPE = ((0, "reply"), (1, "forward"))


class ExerciseTask(MultiTenantMixin, PhishtrayBaseModel):
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
        acceptance_threshold = 4 * (self.score_threshold / 100)
        if score >= acceptance_threshold:
            return self.debrief_over_threshold
        else:
            return self.debrief_under_threshold

    def __str__(self):
        return self.name


class ExerciseFile(MultiTenantMixin, PhishtrayBaseModel):
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


class ExerciseEmailReply(MultiTenantMixin, PhishtrayBaseModel):
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
        return EmailReplyTaskScore.objects.filter(email_reply=self)

    def __str__(self):
        return self.message


class EmailReplyTaskScore(MultiTenantMixin, PhishtrayBaseModel):
    """
    A method to associate scores to email replies.
    """

    value = models.IntegerField()
    email_reply = models.ForeignKey(
        ExerciseEmailReply, on_delete=models.CASCADE, null=True, blank=True
    )
    task = models.ForeignKey(
        ExerciseTask, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return "Reply: {self.email_reply} - {self.task} - {self.value}".format(
            self=self
        )


class ExerciseEmail(MultiTenantMixin, PhishtrayBaseModel):
    def __str__(self):
        return self.subject

    class Meta:
        ordering = ["sort_order"]

    subject = models.CharField(max_length=250, blank=True, null=True)

    # TODO: introduce new model i.e.: Account to store these info
    from_address = models.CharField(max_length=250, blank=True, null=True)
    from_name = models.CharField(max_length=250, blank=True, null=True)
    from_role = models.CharField(max_length=50, blank=True, null=True)

    # TODO: introduce new model i.e.: Account to store these info
    to_address = models.CharField(max_length=250, blank=True, null=True)
    to_name = models.CharField(max_length=250, blank=True, null=True)
    to_role = models.CharField(max_length=50, blank=True, null=True)

    phish_type = models.IntegerField(choices=EXERCISE_PHISH_TYPES)
    phishing_explained = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    attachments = models.ManyToManyField(ExerciseFile, blank=True)
    replies = models.ManyToManyField(ExerciseEmailReply, blank=True)
    belongs_to = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True
    )
    sort_order = models.IntegerField(default=0)

    @property
    def from_account(self):
        data = {
            "email": self.from_address,
            "name": self.from_name,
            "role": self.from_role,
        }
        return data

    @property
    def to_account(self):
        data = {"email": self.to_address, "name": self.to_name, "role": self.to_role}
        return data

    def reveal_time(self, exercise=None):
        email_properties = self.exercise_specific_properties(exercise)
        if email_properties:
            return email_properties.reveal_time

    def exercise_specific_properties(self, exercise=None):
        """
        :param exercise: Exercise instance
        :return: ExerciseEmailProperties instance or None
        """
        email_properties = ExerciseEmailProperties.objects.filter(
            email_id=self.id, exercise=exercise
        ).first()
        return email_properties


class DemographicsInfo(MultiTenantMixin, PhishtrayBaseModel):
    """
    Demographic Questions that can be added to Exercises.
    """

    QUESTION_TYPE_INTEGER = 0
    QUESTION_TYPE_TEXT = 1

    QUESTION_TYPES = ((QUESTION_TYPE_INTEGER, "number"), (QUESTION_TYPE_TEXT, "string"))

    question_type = models.IntegerField(choices=QUESTION_TYPES)
    question = models.CharField(max_length=180, blank=True, null=True)
    required = models.BooleanField(
        help_text="Mark question mandatory on the participant form.", default=False
    )

    class Meta:
        verbose_name_plural = "Demographic Info"

    def __str__(self):
        return self.question


class Exercise(MultiTenantMixin, PhishtrayBaseModel):
    def __str__(self):
        return f"{self.title} - {self.id}"

    user_objects = ExerciseManager()

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    introduction = models.TextField(null=True, blank=True)
    afterword = models.TextField(null=True, blank=True)
    length_minutes = models.IntegerField()
    demographics = models.ManyToManyField(DemographicsInfo, blank=True)
    emails = models.ManyToManyField(ExerciseEmail, blank=True)
    files = models.ManyToManyField(ExerciseFile, blank=True)
    training_link = models.CharField(
        max_length=200,
        blank=True,
        help_text="Defaults to a training URI provided by Cybsafe.",
    )
    debrief = models.BooleanField(
        help_text="Should participants receive a phishing debrief at the end of the exercise?",
        default=False,
    )
    copied_from = models.CharField(max_length=250, null=True, blank=True)
    updated_by = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="updated_by",
    )
    published_by = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="published_by",
    )
    trial_version = models.IntegerField(null=True, blank=True, default=1)
    initial_trial = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="exercise_initial_trial",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["initial_trial", "trial_version"], name="exercise_trial"
            )
        ]

    @property
    def phishing_emails(self):
        return self.emails.filter(phish_type=EXERCISE_EMAIL_PHISH)

    @property
    def phishing_email_ids(self, uuid=False):
        """
        Returns an iterable with phishing email IDs.
        :param uuid: BOOL - when True the function returns UUIDs
        :return: MAP of the email ids as STRING
        """
        phishing_email_ids = self.phishing_emails.values_list("id", flat=True)
        if uuid:
            return phishing_email_ids
        else:
            return map(lambda x: str(x), phishing_email_ids)

    def set_email_reveal_times(self):
        emails = list(self.emails.all())
        if not emails:
            return

        # Set some emails based on a threshold to zero time initially.
        received_emails_count = int(
            ceil((len(emails) * settings.REVEAL_TIME_ZERO_THRESHOLD))
        )

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
            rand_time = int(
                floor(abs(random() - random()) * (1 + self.length_minutes * 60))
            )
            ExerciseEmailProperties.objects.get(
                exercise_id=self.id, email_id=email.id
            ).set_reveal_time(rand_time)

    @property
    def copied_from_exercise_id(self):
        # Expected format of copied_from is 'exercise.name - exercise.id'
        if not self.copied_from:
            return None
        else:
            try:
                return self.copied_from.split(" - ")[1]
            except IndexError:
                return None

    @property
    def copied_from_exercise(self):
        try:
            return Exercise.objects.get(pk=self.copied_from_exercise_id)
        except Exercise.DoesNotExist:
            return None

    def sync_email_properties(self):
        # Generate email properties for the attached emails
        for email in self.emails.all():
            ExerciseEmailProperties.objects.get_or_create(
                exercise_id=self.id, email_id=email.id
            )

        # Remove email properties that are no longer attached to the exercise
        orphaned_email_properties = ExerciseEmailProperties.objects.filter(
            exercise_id=self.id
        ).exclude(email_id__in=self.emails.values_list("id", flat=True))
        if orphaned_email_properties:
            orphaned_email_properties.all().delete()

        # Then set default email reveal times
        self.set_email_reveal_times()


class ExerciseWebPage(MultiTenantMixin, PhishtrayBaseModel):
    PAGE_REGULAR = 0
    PAGE_TYPES = ((PAGE_REGULAR, "regular"),)

    def __str__(self):
        return self.title

    title = models.CharField(max_length=250, blank=True, null=True)
    url = models.CharField(max_length=250, blank=True, null=True)
    type = models.IntegerField(choices=PAGE_TYPES, default=PAGE_REGULAR)
    content = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ("url", "organization")


class ExerciseWebPageReleaseCode(MultiTenantMixin, PhishtrayBaseModel):
    release_code = models.CharField(max_length=250, blank=False, null=False)

    def __str__(self):
        return self.release_code

    class Meta:
        unique_together = ("release_code", "organization")


class ExerciseEmailProperties(PhishtrayBaseModel):
    class Meta:
        unique_together = ("exercise", "email")
        verbose_name_plural = "Exercise email properties"

    objects = ExerciseEmailPropertiesManager()

    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    email = models.ForeignKey(ExerciseEmail, on_delete=models.CASCADE)
    reveal_time = models.PositiveIntegerField(
        blank=True, null=True, help_text="Time in seconds."
    )
    web_page = models.ForeignKey(
        ExerciseWebPage, on_delete=models.CASCADE, null=True, blank=True
    )
    intercept_exercise = models.BooleanField(
        help_text="If selected, participants will be prevented to proceed with the exercise \
        until they enter the correct release code.",
        default=False,
    )
    release_codes = models.ManyToManyField(
        ExerciseWebPageReleaseCode,
        help_text="Accepted codes. \
     Participants, who have been intercepted, will need to provide one of the selected codes \
     to proceed with the exercise.",
        blank=True,
    )
    date_received = models.DateTimeField(
        help_text="If date is provided reveal time will be automatically set to 0.",
        blank=True,
        null=True,
    )

    def set_reveal_time(self, time):
        if self.reveal_time is None:
            self.reveal_time = time
            self.save()

    def save(self, *args, **kwargs):
        if self.date_received is not None:
            self.reveal_time = 0
        super(ExerciseEmailProperties, self).save(*args, **kwargs)
