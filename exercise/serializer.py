from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField
from django.db.models import F

from participant.models import Participant
from participant.serializer import ParticipantActionLogDownloadCSVSerializer
from .models import *


class DemographicsInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DemographicsInfo
        fields = ("id", "question", "question_type", "required")


class ExerciseEmailReplySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExerciseEmailReply
        fields = ("id", "reply_type", "message")


class ExerciseFileSerializer(serializers.HyperlinkedModelSerializer):
    date_created = serializers.DateTimeField(source="created_date")
    file_url = serializers.CharField(source="img_url")

    class Meta:
        model = ExerciseFile
        fields = ("id", "file_name", "description", "date_created", "file_url")


class ExerciseEmailSerializer(serializers.HyperlinkedModelSerializer):
    replies = ExerciseEmailReplySerializer(many=True)
    attachments = ExerciseFileSerializer(many=True)

    class Meta:
        model = ExerciseEmail
        fields = (
            "id",
            "subject",
            "from_address",
            "from_name",
            "to_address",
            "to_name",
            "phish_type",
            "content",
            "attachments",
            "replies",
            "phishing_explained",
        )


class EmailDetailsSerializer(serializers.HyperlinkedModelSerializer):
    replies = ExerciseEmailReplySerializer(many=True)
    attachments = ExerciseFileSerializer(many=True)
    from_account = serializers.SerializerMethodField()
    to_account = serializers.SerializerMethodField()
    body = serializers.CharField(source="content")

    class Meta:
        model = ExerciseEmail
        fields = (
            "id",
            "subject",
            "phish_type",
            "from_account",
            "to_account",
            "body",
            "attachments",
            "replies",
            "phishing_explained",
        )

    def get_from_account(self, email):
        return email.from_account

    def get_to_account(self, email):
        return email.to_account


class ThreadSerializer(serializers.ModelSerializer):
    body = serializers.CharField(source="content")
    from_account = serializers.SerializerMethodField()
    to_account = serializers.SerializerMethodField()
    replies = ExerciseEmailReplySerializer(many=True)
    attachments = ExerciseFileSerializer(many=True)
    emails = serializers.SerializerMethodField()
    reveal_time = serializers.SerializerMethodField()
    thread_properties = serializers.SerializerMethodField()

    class Meta:
        model = ExerciseEmail
        fields = (
            "id",
            "subject",
            "reveal_time",
            "from_account",
            "to_account",
            "body",
            "attachments",
            "replies",
            "emails",
            "phishing_explained",
            "thread_properties",
        )

    def get_emails(self, email):
        belonging_emails_queryset = ExerciseEmail.objects.filter(belongs_to=email.id)
        return EmailDetailsSerializer(belonging_emails_queryset, many=True).data

    def get_from_account(self, email):
        return email.from_account

    def get_to_account(self, email):
        return email.to_account

    def get_reveal_time(self, email):
        return email.reveal_time(exercise=self.context.get("exercise"))

    def get_thread_properties(self, email):
        return ExerciseEmailPropertiesSerializer(
            email.exercise_specific_properties(exercise=self.context.get("exercise"))
        ).data


class ExerciseSerializer(serializers.HyperlinkedModelSerializer):
    threads = serializers.SerializerMethodField()
    profile_form = DemographicsInfoSerializer(source="demographics", many=True)
    files = ExerciseFileSerializer(many=True)

    class Meta:
        model = Exercise
        fields = (
            "id",
            "title",
            "description",
            "introduction",
            "afterword",
            "length_minutes",
            "profile_form",
            "threads",
            "files",
        )

    def get_threads(self, exercise):
        queryset = exercise.emails.all().filter(pk=F("belongs_to"))
        return ThreadSerializer(
            queryset, many=True, context={"exercise": exercise}
        ).data


class ExerciseReportListSerializer(serializers.ModelSerializer):
    exercise_reports_url = HyperlinkedIdentityField(
        view_name="api:exercise-report-detail", lookup_field="pk"
    )

    class Meta:
        model = Exercise
        fields = ("id", "title", "created_date", "exercise_reports_url")


class ExerciseReportSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = ("id", "title", "participants")

    def get_participants(self, exercise):
        serializer_context = {"request": self.context.get("request")}
        participants_queryset = Participant.objects.filter(exercise=exercise)
        serializer = ParticipantActionLogDownloadCSVSerializer(
            participants_queryset, many=True, context=serializer_context
        )
        return serializer.data


class ExerciseWebPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseWebPage
        fields = ("title", "url", "type", "content")


class ExerciseWebPageReleaseCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseWebPageReleaseCode
        fields = ("release_code",)


class ExerciseEmailPropertiesSerializer(serializers.ModelSerializer):
    web_page = ExerciseWebPageSerializer()
    release_codes = ExerciseWebPageReleaseCodeSerializer(many=True)

    class Meta:
        model = ExerciseEmailProperties
        fields = (
            "reveal_time",
            "web_page",
            "intercept_exercise",
            "release_codes",
            "date_received",
        )
