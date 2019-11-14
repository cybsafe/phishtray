from rest_framework.test import APITestCase
from participant.models import Organization, Participant
from participant.factories import OrganizationFactory, ParticipantFactory
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

    def test_org_filter_user_with_organization(self):
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


class ParticipantQuerysetTests(APITestCase):
    def setUp(self):
        organization = OrganizationFactory(name="this_test_organization")
        self.participant1 = ParticipantFactory(organization=organization)
        self.participant2 = ParticipantFactory(organization=organization)
        self.participant3 = ParticipantFactory(organization=organization)

        other_organization = OrganizationFactory(name="other_organization")
        self.participant4 = ParticipantFactory(organization=other_organization)

        self.user = UserFactory(organization=organization)
        self.superuser = UserFactory(organization=organization, is_superuser=True)
        self.user_without_organization = UserFactory()

    def test_participant_filter_by_user_with_organization(self):
        expected_ids = [
            self.participant1.id,
            self.participant2.id,
            self.participant3.id,
        ]
        filtered_ids = Participant.objects.filter_by_user(user=self.user).values_list(
            "id", flat=True
        )

        self.assertEqual(set(expected_ids), set(filtered_ids))

    def test_when_superuser(self):
        all_participants = Participant.objects.all()
        participants = Participant.objects.filter_by_user(user=self.superuser)

        self.assertEqual(list(all_participants), list(participants))

    def test_when_user_without_organization(self):
        participant = Participant.objects.filter_by_user(
            user=self.user_without_organization
        )
        self.assertFalse(participant.exists())

    def test_when_user_is_none(self):
        participant = Participant.objects.filter_by_user(user=None)
        self.assertFalse(participant.exists())

    def test_when_user_is_not_user_instance(self):
        participant = Participant.objects.filter_by_user(
            user="a string or not a user instance"
        )
        self.assertFalse(participant.exists())
