from ..models import Exercise, ExerciseWebPageReleaseCode
from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from exercise.admin import ExerciseAdmin, ExerciseWebPageReleaseCodeAdmin
from django.contrib.admin.options import (
    HORIZONTAL,
    VERTICAL,
    ModelAdmin,
    TabularInline,
    get_content_type_for_model,
)
from exercise.models import Exercise
from exercise.factories import ExerciseFactory, ExerciseWebPageReleaseCodeFactory
from django.contrib import admin
from django.urls import reverse
from users.models import User


class MockRequest:
    pass


class MockSuperUser:
    def __init__(self):
        self.is_superuser = True

    def has_perm(self, perm):
        return True


request = MockRequest()
request.user = MockSuperUser()


class AdminSiteTestsExercise(TestCase):
    def setUp(self):
        self.site = ExerciseAdmin(Exercise, admin.site)
        self.exercise = ExerciseFactory()
        self.username = "cybsafe"
        self.password = "password"
        self.user = User.objects.create_superuser(
            self.username, "cybsafe@phistray.com", self.password
        )

    def test_site_str(self):
        site = ModelAdmin(Exercise, self.site)
        self.assertEqual(str(site), "exercise.ModelAdmin")

    def test_site_fields(self):
        # site = ModelAdmin(Exercise, self.site)
        fields_list = [
            "title",
            "description",
            "introduction",
            "afterword",
            "length_minutes",
            "demographics",
            "emails",
            "files",
            "training_link",
            "debrief",
            "organisation",
            "copied_from",
            "updated_by",
            "published_by",
        ]

        no_readonly_fields = [
            item for item in fields_list if item not in list(self.site.readonly_fields)
        ]
        self.assertEqual(
            set(self.site.get_form(request).base_fields), set(no_readonly_fields)
        )
        self.assertEqual(list(self.site.get_fields(request)), fields_list)
        self.assertEqual(
            list(self.site.get_fields(request, self.exercise)), fields_list
        )
        self.assertIsNone(self.site.get_exclude(request, self.exercise))

    def test_action_copy_exercise(self):
        """
        NO ERRORS:
        In URL. (/admin/exercise/exercise/9e3078cc-f59d-4633-9e6f-63c43191607c/change/)
        Superuser permission True. (Reaching to has_change_permission)
        It is reaching the correct AdminSite
        But not reaching to the correct methods: response_change, save_model
        """

        self.assertEqual(1, Exercise.objects.count())
        data = {"_copy_exercise": ["Copy Exercise"]}
        change_url = reverse("admin:exercise_exercise_change", args=[self.exercise.id])

        # data = {"_selected_action": [self.exercise.id]}
        # change_url = reverse("admin:exercise_exercise_delete", args=[self.exercise.id])

        self.client.login(username=self.username, password=self.password)
        response = self.client.post(change_url, data)
        ex = Exercise.objects.get(id=self.exercise.id)
        print(ex.title)
        print(change_url)
        print(response)
        self.assertEqual(2, Exercise.objects.count())
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(self.exercise.title, Exercise.objects.last().title)


class AdminSiteTestsExerciseWebPageReleaseCode(TestCase):
    """
    THESE TESTS ARE ONLY TO CONFIRM IF ABOVE PROCEDURE IS WORKING ON OTHER ADMIN SITE.
    WHICH IS WORKING
    """

    def setUp(self):
        self.username = "cybsafe"
        self.password = "password"
        self.user = User.objects.create_superuser(
            self.username, "cybsafe@phistray.com", self.password
        )

    def test_action_copy_exercise(self):
        code = ExerciseWebPageReleaseCodeFactory()
        self.assertEqual(1, ExerciseWebPageReleaseCode.objects.count())
        data = {
            "release_code": ["code 1 2 3"],
            "_continue": ["Save and continue editing"],
        }
        change_url = reverse(
            "admin:exercise_exercisewebpagereleasecode_change", args=[code.id]
        )
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(change_url, data)
        self.assertEqual(response.status_code, 302)
        ex = ExerciseWebPageReleaseCode.objects.get(id=code.id)
        print(change_url)
        print(ex.release_code)
        print(response)
