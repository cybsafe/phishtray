from rest_framework import routers
from django.conf.urls import url, include

from .views import (
    ExerciseViewSet,
    ExerciseEmailViewSet,
    ExerciseEmailThreadViewSet,
)

app_name = 'exercise'
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'exercise', ExerciseViewSet, base_name='exercise')
router.register(r'email', ExerciseEmailViewSet, base_name='email')
router.register(r'thread', ExerciseEmailThreadViewSet, base_name='thread')

urlpatterns = router.urls

# urlpatterns = [
#     # path('<slug:link>/profile', views.profile, name='profile'),
#     # path('<slug:link>/start/<int:p_id>/', views.start, name='start'),
#     # path('<slug:link>/', views.index, name='index'),
#     url(r'^', include(router.urls)),
# ]
