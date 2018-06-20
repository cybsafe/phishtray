from django.urls import path

from . import views

from .views import ExerciseViewSet

from rest_framework import routers
from django.conf.urls import url, include


app_name = 'exercise'

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'list', ExerciseViewSet)

exercise_detail = ExerciseViewSet.as_view({
    'get': 'retrieve'
})

exercise_list = ExerciseViewSet.as_view({
    'get': 'list'
})

urlpatterns = [
    path('<slug:link>/profile', views.profile, name='profile'),
    path('<slug:link>/start/<int:p_id>/', views.start, name='start'),
    url('^detail/(?P<pk>[0-9]+)/$', exercise_detail, name='exercise-detail'),
    url('^list/$', exercise_list, name='exercise-list'),
    path('<slug:link>/', views.index, name='index'),
    url(r'^', include(router.urls)),
]
