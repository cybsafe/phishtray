from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.db.models import Q, Value, CharField
from django.db.models.functions import Concat
from exercise.models import Exercise
from .models import Participant


class TrialVersionListFilter(admin.SimpleListFilter):

    title = _("Trial Version")
    parameter_name = "trial_version"

    def lookups(self, request, model_admin):

        exercise = request.GET.get("exercise__id__exact", "")

        if exercise:
            trial_versions = (
                Exercise.user_objects.filter_by_org_private(user=request.user)
                .filter(Q(id=exercise) | Q(initial_trial__id__exact=exercise))
                .annotate(
                    display_name=Concat(
                        "trial_version",
                        Value(" - "),
                        "title",
                        Value(" - "),
                        "id",
                        output_field=CharField(),
                    )
                )
                .order_by("trial_version")
            )
            return trial_versions.values_list("trial_version", "display_name")
        else:
            return Exercise.objects.none()

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


class ExerciseListFilter(admin.SimpleListFilter):

    title = _("Exercise")
    parameter_name = "exercise__id__exact"

    def lookups(self, request, model_admin):

        exercises = (
            Exercise.user_objects.filter_by_org_private(user=request.user)
            .filter(trial_version=1)
            .annotate(
                display_name=Concat(
                    "title", Value(" - "), "id", output_field=CharField()
                )
            )
        )

        return exercises.values_list("id", "display_name")

    def queryset(self, request, queryset):

        return queryset
