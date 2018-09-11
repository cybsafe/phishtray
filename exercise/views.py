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
from participant.models import (
    ActionLog,
    ParticipantAction,
)


# api method to create an action log
# TODO: add url /api/v1/action to this action
def action_logger(request):
    log_data = serializers.deserialize("json", request.POST.get('log_data')).object
    pa = ParticipantAction()
    pa.save()
    a_keys = ['action_type', 'participant_id', 'experiment_id', 'email_id', 'attachment_id']
    for a_key in a_keys:
        if log_data.get(a_key) is not None:
            log = ActionLog(
                action_id=pa.id,
                name=a_key,
                value=log_data.get(a_key)
            )
            log.save()


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
