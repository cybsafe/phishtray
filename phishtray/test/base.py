from users.models import User
from rest_framework.test import APITestCase, APIClient


class PhishtrayAPIBaseTest(APITestCase):
    def setUp(self):
        self.admin_password = "wibble-wobble"
        self.admin_user = User.objects.create_superuser(
            "wibble", "wobble@admin.com", self.admin_password
        )

        self.admin_client = APIClient()
        self.admin_client.login(
            username=self.admin_user.username, password=self.admin_password
        )

        self.client = APIClient()


class ThreadTestsMixin:
    def threadify(self, email, belongs_to=None):
        email.belongs_to = belongs_to or email
        email.save()
