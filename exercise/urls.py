from django.urls import path

from . import views

from .views import ExerciseViewSet

from rest_framework import routers
from django.conf.urls import url, include


app_name = 'exercise'

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'list', ExerciseViewSet)

urlpatterns = [
    path('<slug:link>/profile', views.profile, name='profile'),
    path('<slug:link>/start/<int:p_id>/', views.start, name='start'),
    path('<slug:link>/', views.index, name='index'),
    url(r'^', include(router.urls)),
]
