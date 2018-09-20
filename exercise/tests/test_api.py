from random import randint

from django.urls import reverse
from rest_framework.views import status

from phishtray.test.base import PhishtrayAPIBaseTest
from ..models import Exercise, ExerciseEmail
from ..serializer import ExerciseSerializer, ExerciseEmailSerializer, EmailDetailsSerializer
from djangorestframework_camel_case.util import camelize
from unittest import skip

from ..factories import (
    AttachmentFactory,
    EmailFactory,
    EmailReplyFactory,
    ExerciseFactory,
)


class ExerciseAPITests(PhishtrayAPIBaseTest):

    def setUp(self):
        super(ExerciseAPITests, self).setUp()

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
        self.assertEqual(camelize(serialized.data), response.data)

    def test_get_exercise_details(self):
        """
        Exercise details are public.
        """
        exercise_1 = ExerciseFactory()
        ExerciseFactory.create_batch(5)
        url = reverse('api:exercise-detail', args=[exercise_1.id])

        response = self.client.get(url)

        serialized = ExerciseSerializer(Exercise.objects.get(pk=exercise_1.id))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, serialized.data)

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
        super(EmailAPITestCase, self).setUp()

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
        self.assertEqual(camelize(serialized.data), response.data)

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


class ThreadAPITestCase(PhishtrayAPIBaseTest):

    def setUp(self):
        super(ThreadAPITestCase, self).setUp()

    def test_thread_list_block_public(self):
        """
        Non admin users should not be able to retrieve thread list.
        """
        url = reverse('api:thread-list')
        response = self.client.get(url)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_email_list_allow_admin(self):
        """
        Admin users should be able to retrieve thread list.
        """
        url = reverse('api:thread-list')
        email_count = randint(1, 50)
        emails = EmailFactory.create_batch(email_count)

        email_1 = emails[0]
        email_1.replies.add(EmailReplyFactory())
        email_1.attachments.add(AttachmentFactory())
        email_1.save()

        response = self.admin_client.get(url)
        serialized = EmailDetailsSerializer(ExerciseEmail.objects.all(), many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(email_count, len(response.data))
        self.assertEqual(camelize(serialized.data), response.data)

    @skip
    def test_get_thread_details(self):
        """
        Thread details are public.
        """
        email_1 = EmailFactory()
        email_1.replies.add(EmailReplyFactory())
        email_1.replies.add(EmailReplyFactory())
        email_1.attachments.add(AttachmentFactory())
        email_1.save()
        EmailFactory.create_batch(5)
        url = reverse('api:thread-detail', args=[email_1.id])

        response = self.client.get(url)

        serialized = EmailDetailsSerializer(ExerciseEmail.objects.get(pk=email_1.id))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # TODO: fix assertion (object vs. ordered dict([object]))
        self.assertEqual(response.data, camelize(serialized.data))
        self.assertEqual(2, len(response.data.get('emails')[0].get('replies')))
        self.assertEqual(1, len(response.data.get('emails')[0].get('attachments')))

    def test_get_thread_details_404(self):
        """
        Email details are public.
        """
        EmailFactory.create_batch(5)
        fake_id = 'fakeID'
        url = reverse('api:thread-detail', args=[fake_id])

        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual('Not found.', response.data.get('detail'))
