from django.db import models

from utils import helpers
import django.utils
import json
import uuid


KEY_TYPE_INTEGER = 0
KEY_TYPE_TEXT = 1

EXERCISE_KEY_TYPES = (
    (KEY_TYPE_INTEGER, 'number'),
    (KEY_TYPE_TEXT, 'text'),
)

EXERCISE_EMAIL_PHISH = 0
EXERCISE_EMAIL_REGULAR = 1

EXERCISE_PHISH_TYPES = (
    (EXERCISE_EMAIL_PHISH, 'phishing'),
    (EXERCISE_EMAIL_REGULAR, 'regular'),
    (EXERCISE_EMAIL_REGULAR, 'etray'),
)

EXERCISE_REPLY_TYPE = (
    (0, 'reply'),
    (1, 'forward'),
)

EXERCISE_REPLY_ACTION = 0
EXERCISE_ATTACHMENT_ACTION = 1

EXERCISE_ACTION_TYPES = (
    (EXERCISE_REPLY_ACTION, 'email_reply'),
    (EXERCISE_ATTACHMENT_ACTION, 'email_attachment_open'),
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

    class Meta:
        verbose_name_plural = 'Exercise email replies'


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

    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True)

    @property
    def link(self):
        return helpers.hasher.encode(self.id)


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

    class Meta:
        verbose_name_plural = 'Exercise web pages'


class ExerciseURL(models.Model):

    def __str__(self):
        return self.subject

    id = models.AutoField(primary_key=True)

    subject = models.CharField(max_length=250, blank=True, null=True)
    actual_url = models.CharField(max_length=250, blank=True, null=True)
    real_url = models.CharField(max_length=250, blank=True, null=True)
    type = models.IntegerField(choices=EXERCISE_PHISH_TYPES)

    web_page = models.ForeignKey(ExerciseWebPages, on_delete=models.CASCADE)


class ExerciseAction(models.Model):

    def __str__(self):
        return '{} - {}'.format(self.email, self.get_action_display())

    id = models.AutoField(primary_key=True)

    action = models.IntegerField(choices=EXERCISE_ACTION_TYPES)

    email = models.ForeignKey(ExerciseEmail, on_delete=models.CASCADE)
    reply = models.ForeignKey(ExerciseEmailReply, on_delete=models.CASCADE, null=True, blank=True)
    attachment = models.ForeignKey(ExerciseAttachment, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if (not self.reply and not self.attachment) or (self.reply and self.attachment):
            raise ValueError('Only one reply or attachment need to be populated')
        super().save(*args, **kwargs)
