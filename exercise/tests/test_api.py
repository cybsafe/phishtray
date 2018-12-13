from random import randint

from django.db.models import F
from django.urls import reverse
from rest_framework.views import status
from djangorestframework_camel_case.util import underscoreize

from phishtray.test.base import PhishtrayAPIBaseTest
from ..models import Exercise, ExerciseEmail
from ..serializer import (
    ExerciseSerializer,
    ExerciseEmailSerializer,
    ThreadSerializer,
)
from ..factories import (
    ExerciseFileFactory,
    EmailFactory,
    EmailReplyFactory,
    ExerciseFactory,
)


class ThreadTestsMixin:

    def threadify(self, email):
        email.belongs_to = email
        email.save()


class ExerciseAPITests(PhishtrayAPIBaseTest, ThreadTestsMixin):

    def setUp(self):
        super().setUp()

    def test_exercise_list_block_public(self):
        """
        Non admin users should not be able to retrieve the exercise list.
        """
        url = reverse('api:exercise-list')
        response = self.client.get(url)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_exercise_list_allow_admin(self):
        """
        Admin users should be able to retrieve the exercise list.
        """
        url = reverse('api:exercise-list')
        exercises_count = randint(1, 50)
        ExerciseFactory.create_batch(exercises_count)

        response = self.admin_client.get(url)
        serialized = ExerciseSerializer(Exercise.objects.all(), many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(exercises_count, len(response.data))
        self.assertEqual(serialized.data, underscoreize(response.data))

    def test_get_exercise_details(self):
        """
        Exercise details are public.
        """
        ExerciseFactory.create_batch(5)
        exercise_1 = ExerciseFactory()
        # add emails
        email_count = randint(2, 15)
        emails = EmailFactory.create_batch(email_count)
        self.threadify(emails[0])
        self.threadify(emails[1])
        exercise_1.emails.add(*emails)
        # add files
        file_count = randint(1, 10)
        files = ExerciseFileFactory.create_batch(file_count)
        exercise_1.files.add(*files)
        exercise_1.save()

        url = reverse('api:exercise-detail', args=[exercise_1.id])

        response = self.client.get(url)
        serialized = ExerciseSerializer(Exercise.objects.get(pk=exercise_1.id))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.data.get('threads')))
        self.assertEqual(file_count, len(response.data.get('files')))
        self.assertEqual(serialized.data, underscoreize(response.data))

    def test_get_exercise_details_404(self):
        """
        Exercise details are public.
        """
        ExerciseFactory.create_batch(5)
        fake_id = 'fakeID'
        url = reverse('api:exercise-detail', args=[fake_id])

        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual('Not found.', response.data.get('detail'))


class EmailAPITestCase(PhishtrayAPIBaseTest):

    def setUp(self):
        super().setUp()

    def test_email_list_block_public(self):
        """
        Non admin users should not be able to retrieve the email list.
        """
        url = reverse('api:email-list')
        response = self.client.get(url)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_email_list_allow_admin(self):
        """
        Admin users should be able to retrieve the email list.
        """
        url = reverse('api:email-list')
        email_count = randint(1, 50)
        EmailFactory.create_batch(email_count)

        response = self.admin_client.get(url)
        serialized = ExerciseEmailSerializer(ExerciseEmail.objects.all(), many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(email_count, len(response.data))
        self.assertEqual(serialized.data, underscoreize(response.data))

    def test_get_email_details(self):
        """
        Email details are public.
        """
        email_1 = EmailFactory()
        EmailFactory.create_batch(5)
        url = reverse('api:email-detail', args=[email_1.id])

        response = self.client.get(url)

        serialized = ExerciseEmailSerializer(ExerciseEmail.objects.get(pk=email_1.id))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, serialized.data)

    def test_get_email_details_404(self):
        """
        Email details are public.
        """
        EmailFactory.create_batch(5)
        fake_id = 'fakeID'
        url = reverse('api:email-detail', args=[fake_id])

        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual('Not found.', response.data.get('detail'))


class ThreadAPITestCase(PhishtrayAPIBaseTest, ThreadTestsMixin):

    def setUp(self):
        super().setUp()

    def test_thread_list_block_public(self):
        """
        Non admin users should not be able to retrieve thread list.
        """
        url = reverse('api:thread-list')
        response = self.client.get(url)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_thread_list_allow_admin(self):
        """
        Admin users should be able to retrieve thread list.
        """
        url = reverse('api:thread-list')
        email_count = randint(3, 50)
        emails = EmailFactory.create_batch(email_count)

        self.threadify(emails[0])
        self.threadify(emails[1])

        email_1 = emails[2]
        email_1.replies.add(EmailReplyFactory())
        email_1.attachments.add(ExerciseFileFactory())
        email_1.belongs_to = emails[0]
        email_1.save()

        response = self.admin_client.get(url)
        serialized = ThreadSerializer(
            ExerciseEmail.objects.filter(pk=F('belongs_to')), many=True
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # There should be only 2 threads
        self.assertEqual(2, len(response.data))
        self.assertEqual(serialized.data, underscoreize(response.data))

    def test_get_thread_details(self):
        """
        Thread details are public.
        """

        email_1 = EmailFactory()
        email_1.replies.add(EmailReplyFactory())
        email_1.replies.add(EmailReplyFactory())
        email_1.attachments.add(ExerciseFileFactory())
        # This is how the email becomes a thread (for now...)
        email_1.belongs_to = email_1
        email_1.save()

        # add some emails to email_1 to make it a thread
        email_count = randint(1, 15)
        emails = EmailFactory.create_batch(email_count)

        for email in emails:
            email.belongs_to = email_1
            email.save()

        url = reverse('api:thread-detail', args=[email_1.id])

        response = self.client.get(url)
        serialized = ThreadSerializer(ExerciseEmail.objects.get(pk=email_1.id))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serialized.data, underscoreize(response.data))
        #  +1 because itself will be listed in emails too
        self.assertEqual(email_count + 1, len(response.data.get('emails')))
        self.assertEqual(2, len(response.data.get('replies')))
        self.assertEqual(1, len(response.data.get('attachments')))

    def test_get_thread_details_404(self):
        EmailFactory.create_batch(5)
        fake_id = 'fakeID'
        url = reverse('api:thread-detail', args=[fake_id])

        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual('Not found.', response.data.get('detail'))
