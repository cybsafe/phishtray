from random import randint

import factory
from .models import (
    Exercise,
    ExerciseFile,
    ExerciseEmail,
    ExerciseEmailReply,
    DemographicsInfo,
    ExerciseTask,
    EmailReplyTaskScore,
    ExerciseWebPage,
    ExerciseWebPageReleaseCode,
)


class DemographicsInfoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DemographicsInfo

    question = factory.Sequence(lambda n: "Question {}".format(n + 1))
    question_type = randint(0, 1)


class ExerciseFileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExerciseFile

    file_name = factory.Sequence(lambda n: "testfile_{}.rnd".format(n + 1))
    description = "Wibble wobble."
    img_url = "https://test.image.url/wibble.png"


class EmailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExerciseEmail

    subject = factory.Sequence(lambda n: "Email {}".format(n + 1))
    from_address = "admin@cybsafe.com"
    from_name = "Cybsafe Admin"
    to_address = factory.Sequence(lambda n: "test+{}@cybsafe.com".format(n + 1))
    to_name = factory.Sequence(lambda n: "Some Test User {}".format(n + 1))
    content = factory.Sequence(
        lambda n: "Hi, this is email No. {}. Cheers".format(n + 1)
    )
    phish_type = 0

    @factory.post_generation
    def replies(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of replies were passed in, use them
            self.replies.add(*extracted)


class EmailReplyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExerciseEmailReply

    message = factory.Sequence(lambda n: "Email Reply {}".format(n + 1))
    reply_type = 0


class ExerciseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Exercise

    title = factory.Sequence(lambda n: "Exercise {}".format(n + 1))
    length_minutes = 10

    @factory.post_generation
    def emails(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of emails were passed in, use them
            self.emails.add(*extracted)


class ExerciseTaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExerciseTask


class EmailReplyTaskScoreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmailReplyTaskScore

    email_reply = factory.SubFactory(EmailReplyFactory)


class ExerciseWebPageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExerciseWebPage

    title = factory.Sequence(lambda n: "Page Title {}".format(n + 1))
    url = factory.Sequence(lambda n: "Page URL {}".format(n + 1))
    content = factory.Sequence(lambda n: "Page Content {}".format(n + 1))


class ExerciseWebPageReleaseCodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExerciseWebPageReleaseCode

    release_code = factory.Sequence(lambda n: "Release Code {}".format(n + 1))
