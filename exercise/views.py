from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from participant.models import Participant, ParticipantProfile, STARTED_EXPERIMENT, COMPLETED_EXPERIMENT, \
    OPENED_UNSAFE_EMAIL_LINK, DOWNLOADED_UNSAFE_EMAIL_ATTACHMENT
from participant.helpers import *
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

        request.session['user_data'] = {
            'participant': participant.id,
            'exercise': exercise.id
        }

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
    user_data = serializers.deserialize("json", request.session['user_data']).object
    log_action(type=STARTED_EXPERIMENT, user_data=user_data)
    e_id = helpers.hasher.decode(link)
    exercise = get_object_or_404(Exercise, pk=e_id[0])
    context = {'exercise': exercise, 'exercise_keys': exercise.exercisekey_set.all()}
    return render(request, 'start.html', context)


# api method to log completion of experiment
def complete(request):
    user_data = serializers.deserialize("json", request.session['user_data']).object
    log_action(type=COMPLETED_EXPERIMENT, user_data=user_data)


# api method to log email opened
def open_email(request, email_id):
    user_data = serializers.deserialize("json", request.session['user_data']).object
    user_data['email'] = email_id
    log_action(type=OPENED_UNSAFE_EMAIL_LINK, user_data=user_data)
    request.session['user_data'] = user_data


# api method to log email attachment downloaded
def open_attachment(request, attachment_id):
    user_data = serializers.deserialize("json", request.session['user_data']).object
    user_data['attachment'] = attachment_id
    log_action(type=DOWNLOADED_UNSAFE_EMAIL_ATTACHMENT, user_data=user_data)
    request.session['user_data'] = user_data


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
