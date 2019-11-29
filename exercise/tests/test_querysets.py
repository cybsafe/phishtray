from rest_framework.test import APITestCase
from participant.factories import OrganizationFactory
from users.factories import UserFactory
from ..factories import ExerciseFactory, EmailFactory
from ..models import Exercise, ExerciseEmailProperties


class ExerciseQuerysetTestsByUser(APITestCase):
    def setUp(self):
        self.organization = OrganizationFactory(name="this_test_organization")
        self.organization2 = OrganizationFactory(name="this_test_organization 2")

        self.private_exercise = ExerciseFactory(organization=self.organization)
        self.another_private_exercise = ExerciseFactory(organization=self.organization2)
        self.public_exercise = ExerciseFactory()

        self.user = UserFactory(
            username="user_with_organization", organization=self.organization
        )
        self.superuser = UserFactory(
            organization=self.organization, is_superuser=True, username="test_superuser"
        )
        self.user_without_organization = UserFactory(
            username="user_without_organization"
        )

    def test_exercise_filter_when_user_with_organization(self):
        # The user with organization must see his organization's exercise and public ones
        all_exercises = Exercise.objects.all()
        user_exercises = Exercise.user_objects.filter_by_user(self.user)
        self.assertEqual(3, all_exercises.count())
        self.assertEqual(2, user_exercises.count())

    def test_exercise_filter_when_superuser(self):
        # The superuser must see all exercises
        all_exercises = Exercise.objects.all()
        user_exercises = Exercise.user_objects.filter_by_user(user=self.superuser)

        self.assertEqual(list(all_exercises), list(user_exercises))

    def test_exercises_filter_when_user_without_organization(self):
        # The user without organization must see only public ones
        all_exercises = Exercise.objects.all()
        user_exercises = Exercise.user_objects.filter_by_user(
            user=self.user_without_organization
        )
        self.assertEqual(3, all_exercises.count())
        self.assertEqual(1, user_exercises.count())


class ExerciseQuerysetTestsByOrgPvt(APITestCase):
    def setUp(self):
        self.organization = OrganizationFactory()
        self.organization2 = OrganizationFactory()

        self.private_exercise = ExerciseFactory(organization=self.organization)
        self.org2_exercise = ExerciseFactory(organization=self.organization2)
        self.public_exercise = ExerciseFactory()

        self.user = UserFactory(organization=self.organization)
        self.superuser = UserFactory(organization=self.organization, is_superuser=True)

    def test_exercise_filter_when_user_with_organization(self):
        # The user only sees his own organization's exercise
        all_exercises = Exercise.objects.all()
        user_exercises = Exercise.user_objects.filter_by_org_private(self.user)
        self.assertEqual(3, all_exercises.count())
        self.assertEqual(1, user_exercises.count())

    def test_exercise_filter_when_superuser(self):
        # The superuser must see all exercises
        all_exercises = Exercise.objects.all()
        user_exercises = Exercise.user_objects.filter_by_org_private(
            user=self.superuser
        )

        self.assertEqual(list(all_exercises), list(user_exercises))


class ExerciseEmailPropertiesQuerysetTests(APITestCase):
    def setUp(self):
        self.organization = OrganizationFactory()
        self.organization2 = OrganizationFactory()

        emails = EmailFactory.create_batch(1)
        self.private_exercise = ExerciseFactory(
            organization=self.organization, emails=emails
        )

        self.org2_exercise = ExerciseFactory(
            organization=self.organization2, emails=emails
        )
        self.public_exercise = ExerciseFactory(emails=emails)

        self.user = UserFactory(organization=self.organization)
        self.superuser = UserFactory(organization=self.organization, is_superuser=True)
        self.user_without_organization = UserFactory()

    def test_when_not_superuser(self):
        # The user only gets his own organization's ExerciseEmailProperties
        email_properties = ExerciseEmailProperties.objects.filter_by_org_private(
            self.user
        )

        self.assertEqual(1, email_properties.count())

    def test_when_superuser(self):
        # The superuser must get all ExerciseEmailProperties
        email_properties = ExerciseEmailProperties.objects.filter_by_org_private(
            self.superuser
        )

        self.assertEqual(3, email_properties.count())

    def test_when_user_is_none(self):
        email_properties = ExerciseEmailProperties.objects.filter_by_org_private(None)
        self.assertFalse(email_properties.exists())

    def test_when_user_is_not_user_instance(self):
        email_properties = ExerciseEmailProperties.objects.filter_by_org_private(
            "a string or not a user instance"
        )
        self.assertFalse(email_properties.exists())
