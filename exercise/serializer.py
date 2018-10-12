from rest_framework import serializers

from .models import *


class DemographicsInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DemographicsInfo
        fields = ('id', 'question', 'question_type', 'required')


class ExerciseEmailReplySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExerciseEmailReply
        fields = ('id', 'reply_type', 'message')


class ExerciseFileSerializer(serializers.HyperlinkedModelSerializer):
    date_created = serializers.DateTimeField(source='created_date')
    file_url = serializers.CharField(source='img_url')

    class Meta:
        model = ExerciseFile
        fields = ('id', 'file_name', 'description', 'date_created', 'file_url')


class ExerciseEmailSerializer(serializers.HyperlinkedModelSerializer):
    replies = ExerciseEmailReplySerializer(many=True)
    attachments = ExerciseFileSerializer(many=True)

    class Meta:
        model = ExerciseEmail
        fields = (
            'id',
            'subject',
            'from_address',
            'from_name',
            'to_address',
            'to_name',
            'phish_type',
            'content',
            'attachments',
            'replies',
        )


class EmailDetailsSerializer(serializers.HyperlinkedModelSerializer):
    replies = ExerciseEmailReplySerializer(many=True)
    attachments = ExerciseFileSerializer(many=True)
    from_account = serializers.SerializerMethodField()
    to_account = serializers.SerializerMethodField()
    body = serializers.CharField(source='content')

    class Meta:
        model = ExerciseEmail
        fields = (
            'id',
            'subject',
            'phish_type',
            'from_account',
            'to_account',
            'body',
            'attachments',
            'replies',
        )

    def get_from_account(self, email):
        return email.from_account

    def get_to_account(self, email):
        return email.to_account


class ThreadSerializer(serializers.ModelSerializer):
    body = serializers.CharField(source='content')
    from_account = serializers.SerializerMethodField()
    to_account = serializers.SerializerMethodField()
    replies = ExerciseEmailReplySerializer(many=True)
    attachments = ExerciseFileSerializer(many=True)
    emails = serializers.SerializerMethodField()
    reveal_time = serializers.SerializerMethodField()

    class Meta:
        model = ExerciseEmail
        fields = (
            'id',
            'subject',
            'reveal_time',
            'from_account',
            'to_account',
            'body',
            'attachments',
            'replies',
            'emails',
        )

    def get_emails(self, email):
        belonging_emails_queryset = ExerciseEmail.objects.filter(belongs_to=email.id)
        return EmailDetailsSerializer(belonging_emails_queryset, many=True).data

    def get_from_account(self, email):
        return email.from_account

    def get_to_account(self, email):
        return email.to_account

    def get_reveal_time(self, email):
        return email.reveal_time


class ExerciseSerializer(serializers.HyperlinkedModelSerializer):
    threads = ThreadSerializer(source='emails', many=True)
    profile_form = DemographicsInfoSerializer(source='demographics', many=True)
    files = ExerciseFileSerializer(many=True)

    class Meta:
        model = Exercise
        fields = (
            'id',
            'title',
            'description',
            'introduction',
            'afterword',
            'length_minutes',
            'profile_form',
            'threads',
            'files'
        )
