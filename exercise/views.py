from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import (
    Exercise,
    ExerciseEmail,
)
from .serializer import (
    EmailDetailsSerializer,
    ExerciseSerializer,
    ExerciseEmailSerializer,
)


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
    serializer_class = EmailDetailsSerializer

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
