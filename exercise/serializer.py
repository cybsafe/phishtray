from rest_framework import serializers
from exercise.models import *


class ExerciseEmailReplySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExerciseEmailReply
        fields = ('id', 'content')


class ExerciseAttachmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExerciseAttachment
        fields = ('id', 'filename', 'created_date', 'modified_date')


class ExerciseEmailSerializer(serializers.HyperlinkedModelSerializer):
    replies = ExerciseEmailReplySerializer(many=True)
    attachments = ExerciseAttachmentSerializer(many=True)

    class Meta:
        model = ExerciseEmail
        fields = ('id', 'subject', 'from_address', 'from_name', 'type', 'content','attachments', 'replies')


class ExerciseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Exercise
        fields = ('id', 'title', 'description', 'introduction', 'afterword', 'length_minutes',
                  'created_date', 'modified_date')