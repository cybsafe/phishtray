from django.db import models

from picklefield.fields import PickledObjectField
from random import randint

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


class ExerciseAttachment(PhishtrayBaseModel):
    filename = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.filename


class ExerciseEmailReply(PhishtrayBaseModel):
    reply_type = models.IntegerField(choices=EXERCISE_REPLY_TYPE, null=True)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.message


class ExerciseEmail(PhishtrayBaseModel):

    def __str__(self):
        return self.subject

    subject = models.CharField(max_length=250, blank=True, null=True)
    from_address = models.CharField(max_length=250, blank=True, null=True)
    from_name = models.CharField(max_length=250, blank=True, null=True)
    to_address = models.CharField(max_length=250, blank=True, null=True)
    to_name = models.CharField(max_length=250, blank=True, null=True)

    phish_type = models.IntegerField(choices=EXERCISE_PHISH_TYPES)
    content = models.TextField(null=True, blank=True)
    attachments = models.ManyToManyField(ExerciseAttachment, blank=True)
    replies = models.ManyToManyField(ExerciseEmailReply, blank=True)
    belongs_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)


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
    email_reveal_times = PickledObjectField(null=True)

    def set_email_reveal_times(self):
        # generate email reveal times - these are unique per exercise and are stored in seconds
        # TODO: (TCKT-1235) minimum amount of emails that should have reveal_time 0
        # in case the 10% of emails is less than 1 email
        reveal_times = []

        emails = self.emails.all()
        if not emails:
            return

        for email in emails:
            reveal_times.append(
                {
                    'email_id': email.id,
                    'reveal_time':  randint(0, self.length_minutes * 60)
                }
            )

        # Make 10% of emails appear in inbox at the beginning of exercise
        received_emails_count = int(emails.count() * 0.1)
        if received_emails_count >= 1:
            updated_reveal_times = []

            while received_emails_count:
                received_email = reveal_times.pop(randint(0, len(reveal_times)-1))
                received_email['reveal_time'] = 0
                updated_reveal_times.append(received_email)
                received_emails_count -= 1

            reveal_times += updated_reveal_times

        self.email_reveal_times = reveal_times


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
