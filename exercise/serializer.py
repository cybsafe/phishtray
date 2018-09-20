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


class ExerciseAttachmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExerciseAttachment
        fields = ('id', 'filename')


class ExerciseEmailSerializer(serializers.HyperlinkedModelSerializer):
    replies = ExerciseEmailReplySerializer(many=True)
    attachments = ExerciseAttachmentSerializer(many=True)

    class Meta:
        model = ExerciseEmail
        fields = ('id', 'subject', 'from_address', 'from_name', 'to_address', 'to_name', 'phish_type',
                  'content','attachments', 'replies')


class EmailDetailsSerializer(serializers.HyperlinkedModelSerializer):
    replies = ExerciseEmailReplySerializer(many=True)
    attachments = ExerciseAttachmentSerializer(many=True)
    from_account = serializers.SerializerMethodField()
    to_account = serializers.SerializerMethodField()
    body = serializers.CharField(source='content')

    class Meta:
        model = ExerciseEmail
        fields = ('id', 'subject', 'phish_type', 'from_account', 'to_account',
                  'body', 'attachments', 'replies')

    def get_from_account(self, email):
        return email.from_account

    def get_to_account(self, email):
        return email.to_account


class ThreadSerializer(serializers.ModelSerializer):
    body = serializers.CharField(source='content')
    from_account = serializers.SerializerMethodField()
    to_account = serializers.SerializerMethodField()
    replies = ExerciseEmailReplySerializer(many=True)
    attachments = ExerciseAttachmentSerializer(many=True)
    emails = serializers.SerializerMethodField()

    class Meta:
        model = ExerciseEmail
        fields = ('id', 'subject', 'from_account', 'to_account', 'body', 'attachments', 'replies', 'emails')

    def get_emails(self, email):
        belonging_emails_queryset = ExerciseEmail.objects.filter(belongs_to=email.id)
        return EmailDetailsSerializer(belonging_emails_queryset, many=True).data

    def get_from_account(self, email):
        return email.from_account

    def get_to_account(self, email):
        return email.to_account


class ExerciseSerializer(serializers.HyperlinkedModelSerializer):
    threads = ThreadSerializer(source='emails', many=True)
    email_reveal_times = serializers.SerializerMethodField()
    profile_form = DemographicsInfoSerializer(source='demographics', many=True)

    class Meta:
        model = Exercise
        fields = ('id', 'title', 'description', 'introduction', 'afterword', 'length_minutes',
                  'profile_form', 'threads', 'email_reveal_times')

    def get_email_reveal_times(self, obj):
        # Attempt to generate reveal times if it's missing
        if not obj.email_reveal_times:
            obj.set_email_reveal_times()
            obj.save()
        return obj.email_reveal_times
