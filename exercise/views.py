import csv

from django.db.models import F
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from participant.models import Participant
from participant.serializer import ParticipantActionLogToCSVSerializer
from .models import Exercise, ExerciseEmail
from .serializer import (
    ExerciseSerializer,
    ExerciseEmailSerializer,
    ExerciseReportSerializer,
    ExerciseReportListSerializer,
    ThreadSerializer,
)


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    http_method_names = ("get", "head", "options")

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "list":
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    @action(methods=["GET"], detail=True, permission_classes=[])
    def init(self, request, *args, **kwargs):
        exercise = self.get_object()
        participant = Participant.objects.create(
            exercise=exercise, organization=exercise.organization
        )
        resp = {
            "participant": str(participant.id),
            "exercise": ExerciseSerializer(exercise).data,
        }
        return Response(data=resp)


class ExerciseEmailViewSet(viewsets.ModelViewSet):
    queryset = ExerciseEmail.objects.all()
    serializer_class = ExerciseEmailSerializer
    http_method_names = ("get", "head", "options")

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "list":
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


class ExerciseEmailThreadViewSet(viewsets.ModelViewSet):
    """
    This view retrieves emails in thread style
    """

    queryset = ExerciseEmail.objects.filter(pk=F("belongs_to"))
    serializer_class = ThreadSerializer
    http_method_names = ("get", "head", "options")

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "list":
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


class ExerciseReportViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all().order_by("-created_date")
    http_method_names = ("get", "head", "options")
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get_serializer_class(self):
        if self.action == "list":
            return ExerciseReportListSerializer
        return ExerciseReportSerializer

    def get_serializer_context(self):
        context = super(ExerciseReportViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    @action(
        methods=["get"],
        detail=True,
        permission_classes=[IsAuthenticated, IsAdminUser],
        url_path="download-csv",
        url_name="download_csv",
    )
    def download_csv(self, *args, **kwargs):
        participant_id = self.request.query_params.get("participant")
        participant = Participant.objects.filter(pk=participant_id).first()

        if not participant:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ParticipantActionLogToCSVSerializer(participant)
        csv_data = serializer.data.get("csv")

        file_name = "participant_{}_PID_{}.csv".format(participant_id, participant.pid)
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="{}"'.format(file_name)

        writer = csv.writer(response)
        writer.writerow(csv_data["headers"])

        for row in csv_data["rows"]:
            writer.writerow(row)

        return response
