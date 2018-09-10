import factory
from . import models


class EmailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ExerciseEmail

    subject = factory.Sequence(lambda n: 'Email {}'.format(n+1))
    phish_type = 0


class ExerciseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Exercise

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
