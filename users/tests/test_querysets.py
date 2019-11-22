from rest_framework.test import APITestCase
from users.models import User
from participant.factories import OrganizationFactory
from users.factories import UserFactory


class UserQuerysetTests(APITestCase):
    def setUp(self):
        self.organization = OrganizationFactory()
        self.other_organization = OrganizationFactory()
        self.user1 = UserFactory(organization=self.organization)
        self.user2 = UserFactory(organization=self.organization)
        self.superuser = UserFactory(organization=self.organization, is_superuser=True)
        self.user_of_other_organization = UserFactory(
            organization=self.other_organization
        )

    def test_a_user(self):
        users = User.objects.filter_by_org_private(user=self.user1)
        user_organizations = users.values_list("organization__name", flat=True)

        self.assertEqual(3, users.count())
        self.assertTrue(self.organization.name in user_organizations)
        self.assertFalse(self.other_organization.name in user_organizations)

    def test_a_superuser(self):
        users = User.objects.filter_by_org_private(user=self.superuser)
        user_organizations = users.values_list("organization__name", flat=True)

        self.assertEqual(4, users.count())
        self.assertTrue(self.organization.name in user_organizations)
        self.assertTrue(self.other_organization.name in user_organizations)

    def test_when_user_is_none(self):
        user = User.objects.filter_by_org_private(user=None)
        self.assertFalse(user.exists())

    def test_when_user_is_not_user_instance(self):
        user = User.objects.filter_by_org_private(user=None)
        self.assertFalse(user.exists())
