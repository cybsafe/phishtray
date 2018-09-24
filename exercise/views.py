from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from participant.models import Participant
from .models import (
    Exercise,
    ExerciseEmail,
)
from .serializer import (
    ExerciseSerializer,
    ExerciseEmailSerializer,
    ThreadSerializer)


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    http_method_names = ['get', 'head', 'options']

    @action(methods=['get'], detail=True, permission_classes=[])
    def init(self, request, *args, **kwargs):
        exercise = self.get_object()
        participant = Participant(exercise=exercise)
        participant.save()
        resp = {
            'participant': str(participant.id),
            'exercise': ExerciseSerializer(exercise).data
        }
        return Response(data=resp)


class ExerciseEmailViewSet(viewsets.ModelViewSet):
    queryset = ExerciseEmail.objects.all()
    serializer_class = ExerciseEmailSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    http_method_names = ['get', 'head', 'options']


class ExerciseEmailThreadViewSet(viewsets.ModelViewSet):
    """
    This view retrieves emails in thread style
    """
    queryset = ExerciseEmail.objects.all()
    serializer_class = ThreadSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    http_method_names = ['get', 'head', 'options']
