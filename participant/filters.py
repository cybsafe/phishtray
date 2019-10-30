from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.db.models import Q
from exercise.models import Exercise
from .models import Participant


class TrialVersionListFilter(admin.SimpleListFilter):

    title = _("trial version")
    parameter_name = "trial_version"

    def lookups(self, request, model_admin):

        exercise = request.GET.get("exercise__id__exact", "")
        print(exercise)

        if exercise:
            trial_versions = (
                Exercise.user_objects.filter_by_user(user=request.user)
                .filter(Q(id=exercise) | Q(initial_trial__id__exact=exercise))
                .order_by("trial_version")
            )
            print(len(trial_versions))
        else:
            trial_versions = Exercise.objects.none()

        return trial_versions.values_list("trial_version", "trial_version")

    def queryset(self, request, queryset):

        queryset = Participant.objects.filter_by_user(user=request.user)
        exercise = request.GET.get("exercise__id__exact", None)
        trial_version = request.GET.get("trial_version", None)

        if exercise and not trial_version:
            return queryset.filter(
                Q(exercise_id=exercise) | Q(exercise__initial_trial__id__exact=exercise)
            )

        if exercise and trial_version:
            return queryset.filter(
                (
                    Q(exercise_id=exercise)
                    | Q(exercise__initial_trial__id__exact=exercise)
                ),
                exercise__trial_version=trial_version,
            )

        return queryset
