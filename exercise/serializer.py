from rest_framework import serializers
from exercise.models import *


class ExerciseEmailReplySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExerciseEmailReply
        fields = ('id', 'reply_type', 'message')


class ExerciseAttachmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExerciseAttachment
        fields = ('id', 'filename', 'created_date', 'modified_date')


class ExerciseEmailSerializer(serializers.HyperlinkedModelSerializer):
    replies = ExerciseEmailReplySerializer(many=True)
    attachments = ExerciseAttachmentSerializer(many=True)

    class Meta:
        model = ExerciseEmail
        fields = ('id', 'subject', 'from_address', 'from_name', 'to_address', 'to_name', 'phish_type',
                  'content','attachments', 'replies')


class EmailCoverSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExerciseEmail
        fields = ('id', 'subject', 'from_address', 'from_name')


class EmailDetailsSerializer(serializers.HyperlinkedModelSerializer):
    replies = ExerciseEmailReplySerializer(many=True)
    attachments = ExerciseAttachmentSerializer(many=True)

    class Meta:
        model = ExerciseEmail
        fields = ('id', 'subject', 'from_address', 'from_name', 'to_address', 'to_name', 'phish_type',
                  'content','attachments', 'replies')

    def to_representation(self, obj):
        data = EmailCoverSerializer().to_representation(obj)
        emails = list()
        emails.append(super(EmailDetailsSerializer, self).to_representation(obj))
        emails = self.process_email_chain(data['id'], emails)
        data['emails'] = emails
        return data

    def process_email_chain(self, id, emails):
        belongs_to = id
        while belongs_to is not None:
            try:
                chain_email = ExerciseEmail.objects.get(belongs_to_id=belongs_to)
                emails.append(super(EmailDetailsSerializer, self).to_representation(chain_email))
                belongs_to = chain_email.id
            except Exception:
                belongs_to = None
        return emails

class ExerciseEmailsThroughSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='exerciseemail.id')
    subject = serializers.ReadOnlyField(source='exerciseemail.subject')
    from_address = serializers.ReadOnlyField(source='exerciseemail.from_address')
    from_name = serializers.ReadOnlyField(source='exerciseemail.from_name')
    to_address = serializers.ReadOnlyField(source='exerciseemail.to_address')
    to_name = serializers.ReadOnlyField(source='exerciseemail.to_name')
    phish_type = serializers.ReadOnlyField(source='exerciseemail.phish_type')
    content = serializers.ReadOnlyField(source='exerciseemail.content')

    replies = ExerciseEmailReplySerializer(source='exerciseemail.replies', many=True, read_only=True)
    attachments = ExerciseAttachmentSerializer(source='exerciseemail.attachments', many=True, read_only=True)

    class Meta:
        model = ExerciseEmailsThrough
        fields = ('id', 'subject', 'from_address', 'from_name', 'to_address', 'to_name', 'phish_type',
                  'content','reveal_time','attachments', 'replies',)

class ExerciseSerializer(serializers.HyperlinkedModelSerializer):
    #emails = ExerciseEmailSerializer(many=True)
    emails = ExerciseEmailsThroughSerializer(source='exerciseemailsthrough_set', many=True)

    class Meta:
        model = Exercise
        fields = ('id', 'title', 'description', 'introduction', 'afterword', 'length_minutes', 'emails',
                  'created_date', 'modified_date')

