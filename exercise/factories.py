import factory
from .models import (
    Exercise,
    ExerciseAttachment,
    ExerciseEmail,
    ExerciseEmailReply,
)


class AttachmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExerciseAttachment

    filename = factory.Sequence(lambda n: 'filename_{}.rnd'.format(n+1))


class EmailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExerciseEmail

    subject = factory.Sequence(lambda n: 'Email {}'.format(n+1))
    from_address = 'admin@cybsafe.com'
    from_name = 'Cybsafe Admin'
    to_address = factory.Sequence(lambda n: 'test+{}@cybsafe.com'.format(n + 1))
    to_name = factory.Sequence(lambda n: 'Some Test User {}'.format(n + 1))
    content = factory.Sequence(lambda n: 'Hi, this is email No. {}. Cheers'.format(n+1))
    phish_type = 0


class EmailReplyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExerciseEmailReply

    message = factory.Sequence(lambda n: 'Email Reply {}'.format(n+1))
    reply_type = 0


class ExerciseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Exercise

    title = factory.Sequence(lambda n: 'Exercise {}'.format(n+1))
    length_minutes = 10

    @factory.post_generation
    def emails(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of emails were passed in, use them
            for email in extracted:
                self.emails.add(email)
