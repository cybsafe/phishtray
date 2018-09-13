from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from participant.models import Participant, ParticipantProfile, ParticipantAction, ActionLog
from utils import helpers
from rest_framework import serializers, viewsets
from exercise.serializer import *


def index(request, link):
    e_id = helpers.hasher.decode(link)
    exercise = get_object_or_404(Exercise, pk=e_id[0])
    context = {'exercise': exercise}
    return render(request, 'index.html', context)


def profile(request, link):
    e_id = helpers.hasher.decode(link)
    exercise = get_object_or_404(Exercise, pk=e_id[0])
    profile_keys = exercise.exercisekey_set.all()

    if request.method == 'POST':
        # try:
        participant = Participant(
            exercise=exercise,
        )
        participant.save()

        for key in profile_keys:
            ParticipantProfile(
                participant=participant,
                key=key,
                value=request.POST[key.key]
            ).save()

        p_id = participant.id
        return HttpResponseRedirect(reverse('exercise:start', args=(link, p_id)))
    else:
        context = {'exercise': exercise, 'exercise_keys': profile_keys}
        return render(request, 'profile.html', context)


def start(request, link, p_id):
    e_id = helpers.hasher.decode(link)
    exercise = get_object_or_404(Exercise, pk=e_id[0])
    context = {'exercise': exercise, 'exercise_keys': exercise.exercisekey_set.all()}
    return render(request, 'start.html', context)


# api method to create an action log
# TODO: add url /api/v1/action to this action
def action_logger(request):
    log_data = serializers.deserialize("json", request.POST.get('log_data')).object
    pa = ParticipantAction.create()
    pa.save()
    a_keys = ['action_type', 'participant_id', 'experiment_id', 'email_id', 'attachment_id']
    for a_key in a_keys:
        if log_data.get(a_key) is not None:
            log = ActionLog.create(
                action_id=pa.id,
                name=a_key,
                value=log_data.get(a_key)
            )
            log.save()


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer


class ExerciseEmailViewSet(viewsets.ModelViewSet):
    queryset = ExerciseEmail.objects.all()
    serializer_class = ExerciseEmailSerializer


class ExerciseEmailThreadViewSet(viewsets.ModelViewSet):
    """
    This view retrieves emails in thread style
    """
    queryset = ExerciseEmail.objects.all()
    serializer_class = EmailDetailsSerializer
