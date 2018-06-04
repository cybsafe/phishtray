from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from exercise.models import Exercise
from participant.models import Participant, ParticipantProfile
from utils import helpers
from rest_framework import serializers, viewsets


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


class ExerciseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Exercise
        fields = ('id', 'title', 'description', 'introduction', 'afterword', 'length_minutes',
                  'created_date', 'modified_date')


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
