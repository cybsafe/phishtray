from rest_framework.test import APITestCase
from participant.factories import OrganizationFactory
from users.factories import UserFactory
from ..factories import ExerciseFactory
from ..models import Exercise


class ExerciseQuerysetTests(APITestCase):
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
