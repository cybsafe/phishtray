from rest_framework.test import APITestCase
from participant.models import Organization
from participant.factories import OrganizationFactory
from users.factories import UserFactory


class OrganizationQuerysetTests(APITestCase):
    def setUp(self):
        self.organization = OrganizationFactory(name="this_test_organization")
        self.organization2 = OrganizationFactory(name="this_test_organization 2")
        self.organization3 = OrganizationFactory(name="this_test_organization 3")
        self.user = UserFactory(
            username="user_with_organization", organization=self.organization
        )
        self.superuser = UserFactory(
            organization=self.organization, is_superuser=True, username="test_superuser"
        )
        self.user_without_organization = UserFactory(
            username="user_without_organization"
        )

    def test_org_filter__user_with_organization(self):
        organization = Organization.objects.filter_by_user(user=self.user)
        self.assertEqual(1, organization.count())
        self.assertEqual("this_test_organization", self.organization.name)

    def test_when_superuser(self):
        all_organizations = Organization.objects.all()
        organizations = Organization.objects.filter_by_user(user=self.superuser)

        self.assertEqual(list(all_organizations), list(organizations))

    def test_when_user_without_organization(self):
        organization = Organization.objects.filter_by_user(
            user=self.user_without_organization
        )
        self.assertFalse(organization.exists())

    def test_when_user_is_none(self):
        organization = Organization.objects.filter_by_user(user=None)
        self.assertFalse(organization.exists())

    def test_when_user_is_not_user_instance(self):
        organization = Organization.objects.filter_by_user(
            user="a string or not a user instance"
        )
        self.assertFalse(organization.exists())
