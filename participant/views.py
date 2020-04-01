from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from exercise.models import DemographicsInfo
from .models import ActionLog, Participant, ParticipantAction, ParticipantProfileEntry
from .serializer import ParticipantSerializer, ParticipantScoreSerializer


class ParticipantViewSet(viewsets.ModelViewSet):
    """
    Viewset to provide POST endpoint to submit demographic information.
    POST is unrestricted as long as the participant ID is valid.
    """

    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "list":
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    http_method_names = ["get", "post", "head", "options"]

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[],
        url_path="extend-profile",
        url_name="extend_profile",
    )
    def extend_profile(self, request, *args, **kwargs):
        # If there's nothing to update cut short
        profile_entries = request.data.get("profile_form", [])
        if not profile_entries:
            return Response()

        participant = self.get_object()
        new_entries = []
        invalid_demographics_ids = []

        for entry in profile_entries:
            demo_id = entry.get("id")
            answer = entry.get("value")

            if demo_id:
                try:
                    demographics_info = DemographicsInfo.objects.get(pk=demo_id)
                except DemographicsInfo.DoesNotExist:
                    invalid_demographics_ids.append(demo_id)
                else:
                    profile_entry = ParticipantProfileEntry(
                        demographics_info=demographics_info, answer=answer
                    )
                    profile_entry.save()
                    new_entries.append(profile_entry)

        if new_entries:
            participant.profile.add(*new_entries)
            participant.save()

        if invalid_demographics_ids:
            resp = {
                "message": "Participant profile has been partially updated due to errors.",
                "errors": [
                    {
                        "message": "Missing or invalid demographics IDs.",
                        "id_list": invalid_demographics_ids,
                    }
                ],
            }
        else:
            resp = {"message": "Participant profile has been successfully updated."}

        return Response(data=resp)

    @action(methods=["post"], detail=True, permission_classes=[])
    def action(self, request, *args, **kwargs):

        if len(request.data) == 0:
            resp = {"message": "Nothing to log."}
            return Response(data=resp)

        participant_action = ParticipantAction.objects.create(
            participant_id=kwargs["pk"]
        )

        action_log_items = []
        complex_keys = []

        for key, value in request.data.items():
            # Skip complex structures
            if isinstance(value, dict) or isinstance(value, list):
                complex_keys.append(key)
                continue
            else:
                action_log_items.append(
                    ActionLog(action=participant_action, name=key, value=value)
                )

        ActionLog.objects.bulk_create(action_log_items)

        if not complex_keys:
            resp = {"message": "Action has been logged successfully."}
        else:
            resp = {
                "message": "Action has been partially logged. Cannot log complex data types.",
                "skipped": complex_keys,
            }

        resp["action_id"] = str(participant_action.id)
        return Response(data=resp)


class ParticipantScoreViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantScoreSerializer
