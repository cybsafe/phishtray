import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from exercise.models import Exercise, ExerciseEmail, ExerciseEmailReply, ExerciseAttachment, ExerciseAction, EXERCISE_ACTION_TYPES, EXERCISE_REPLY_ACTION, EXERCISE_ATTACHMENT_ACTION
from participant.models import Participant, ParticipantProfile
from utils import helpers
from rest_framework import serializers, viewsets
from exercise.serializer import *

ACTION_TYPES = [action_type[1] for action_type in EXERCISE_ACTION_TYPES]

ACTION_JSON_SCHEMA = {
    'type': 'object',
    'properties': {
        'milliseconds': {
            'type': 'number',
            'minimum': 0,
        },
        'action': {
            'type': 'object',
            'properties': {
                'type': {
                    'type': 'string',
                    'pattern': '^{0}$'.format('|'.join(ACTION_TYPES)),
                },
                'associations': {
                    'type': 'object',
                    'properties': {
                        'exerciseEmail': {
                            'type': 'number',
                            'minimum': 0,
                        },
                        'exerciseEmailReply': {
                            'type': 'number',
                            'minimum': 0,
                        },
                        'exerciseAttachment': {
                            'type': 'number',
                            'minimum': 0,
                        },
                    },
                    'required': ['exerciseEmail'],
                },
            },
            'required': ['type', 'associations'],
        },
    },
    'required': ['milliseconds', 'action'],
}


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


@csrf_exempt
@require_http_methods(['POST'])
def store_action(request):
    body = request.body
    content = json.loads(body)

    # validate json format
    try:
        validate(content, ACTION_JSON_SCHEMA)
    except ValidationError:
        return JsonResponse({'message': 'Json validation error', 'status': False}, status=500)

    try:
        action_type = content['action']['type']
        associations = content['action']['associations']
        exercise_email_id = associations['exerciseEmail']

        action = None
        exercise_email_reply = None
        exercise_attachment = None
        exercise_email = ExerciseEmail.objects.get(id=exercise_email_id)

        # get the reply or attachment instance corresponding to the action
        if action_type == 'email_reply' and 'exerciseEmailReply' in associations:
            exercise_email_reply = ExerciseEmailReply.objects.get(id=associations['exerciseEmailReply'])
            action = EXERCISE_REPLY_ACTION
        elif action_type == 'email_attachment_open' and 'exerciseAttachment' in associations:
            exercise_attachment = ExerciseAttachment.objects.get(id=associations['exerciseAttachment'])
            action = EXERCISE_ATTACHMENT_ACTION

        exercise_action = ExerciseAction(
            action = action,
            email = exercise_email,
            reply = exercise_email_reply,
            attachment = exercise_attachment,
        )
        exercise_action.save()
    except ExerciseEmail.DoesNotExist:
        return JsonResponse({'message': 'Invalid email id', 'status': False}, status=500)
    except ExerciseEmailReply.DoesNotExist:
        return JsonResponse({'message': 'Invalid email reply id', 'status': False}, status=500)
    except ExerciseAttachment.DoesNotExist:
        return JsonResponse({'message': 'Invalid attachement id', 'status': False}, status=500)

    return JsonResponse({'message': None, 'status': False}, status=200)
