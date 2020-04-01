from rest_framework import routers

from exercise.views import (
    ExerciseViewSet,
    ExerciseEmailViewSet,
    ExerciseEmailThreadViewSet,
    ExerciseReportViewSet,
)

from participant.views import ParticipantViewSet, ParticipantScoreViewSet

app_name = "api"
router = routers.DefaultRouter()
router.register(r"emails", ExerciseEmailViewSet, basename="email")
router.register(r"exercises", ExerciseViewSet, basename="exercise")
router.register(r"exercise-reports", ExerciseReportViewSet, basename="exercise-report")
router.register(r"participants", ParticipantViewSet, basename="participant")
router.register(
    r"participant-scores", ParticipantScoreViewSet, basename="participant-score"
)
router.register(r"threads", ExerciseEmailThreadViewSet, basename="thread")

urlpatterns = router.urls
