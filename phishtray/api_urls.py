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
router.register(r"emails", ExerciseEmailViewSet, base_name="email")
router.register(r"exercises", ExerciseViewSet, base_name="exercise")
router.register(r"exercise-reports", ExerciseReportViewSet, base_name="exercise-report")
router.register(r"participants", ParticipantViewSet, base_name="participant")
router.register(
    r"participant-scores", ParticipantScoreViewSet, base_name="participant-score"
)
router.register(r"threads", ExerciseEmailThreadViewSet, base_name="thread")

urlpatterns = router.urls
