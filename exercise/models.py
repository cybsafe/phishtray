from django.db import models
from django.core.exceptions import ValidationError

from picklefield.fields import PickledObjectField
from random import randint
from utils import helpers


KEY_TYPE_INTEGER = 0
KEY_TYPE_TEXT = 1

EXERCISE_KEY_TYPES = (
    (KEY_TYPE_INTEGER, 'number'),
    (KEY_TYPE_TEXT, 'text'),
)

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


class ExerciseAttachment(models.Model):

    def __str__(self):
        return self.filename

    id = models.AutoField(primary_key=True)

    filename = models.CharField(max_length=250, blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True)


class ExerciseEmailReply(models.Model):

    def __str__(self):
        return self.message

    id = models.AutoField(primary_key=True)

    reply_type = models.IntegerField(choices=EXERCISE_REPLY_TYPE, null=True)

    message = models.TextField(null=True, blank=True)


class ExerciseEmail(models.Model):

    def __str__(self):
        return self.subject

    id = models.AutoField(primary_key=True)

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

    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    deleted = models.BooleanField(default=False)

    # don't allow overwrite once published
    published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.published:
            raise ValidationError("You may not edit an existing %s" % self._meta.model_name)
        super(ExerciseEmail, self).save(*args, **kwargs)


class Exercise(models.Model):

    def __str__(self):
        return self.title

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    introduction = models.TextField(null=True, blank=True)
    afterword = models.TextField(null=True, blank=True)

    length_minutes = models.IntegerField()
    emails = models.ManyToManyField(ExerciseEmail, blank=True)
    email_reveal_times = PickledObjectField(null=True)

    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    deleted = models.BooleanField(default=False)

    # don't allow overwrite once published
    published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.published:
            raise ValidationError("You may not edit an existing %s" % self._meta.model_name)

        if not self.pk:
            super(Exercise, self).save(*args, **kwargs)
        else:
            # Set reveal time for emails in this exercise
            # Only set this if this wasn't generated before!
            # TODO: (TCKT-1234) introduce a field to record state for an exercise e.g.: "live"
            # reveal_times could be regenerated until the exercise get to a certain state
            if not self.email_reveal_times:
                self.set_email_reveal_times()
            super(Exercise, self).save(*args, **kwargs)

    @property
    def link(self):
        return helpers.hasher.encode(self.id)

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


class ExerciseKey(models.Model):

    def __str__(self):
        return self.key

    id = models.AutoField(primary_key=True)
    exercise = models.ManyToManyField(Exercise)

    type = models.IntegerField(choices=EXERCISE_KEY_TYPES)
    key = models.CharField(max_length=180, blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True)

    @property
    def html5_type(self):
        return EXERCISE_KEY_TYPES[self.type][1]


class ExerciseWebPages(models.Model):

    def __str__(self):
        return self.subject

    id = models.AutoField(primary_key=True)

    subject = models.CharField(max_length=250, blank=True, null=True)
    url = models.CharField(max_length=250, blank=True, null=True)
    type = models.IntegerField(choices=EXERCISE_PHISH_TYPES)
    content = models.TextField(null=True, blank=True)


class ExerciseURL(models.Model):

    def __str__(self):
        return self.subject

    id = models.AutoField(primary_key=True)

    subject = models.CharField(max_length=250, blank=True, null=True)
    actual_url = models.CharField(max_length=250, blank=True, null=True)
    real_url = models.CharField(max_length=250, blank=True, null=True)
    type = models.IntegerField(choices=EXERCISE_PHISH_TYPES)

    web_page = models.ForeignKey(ExerciseWebPages, on_delete=models.CASCADE)
