from django.urls import path

from . import views

from .views import *

from rest_framework import routers
from django.conf.urls import url, include


app_name = 'exercise'

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'list', ExerciseViewSet)

exercise_list = ExerciseViewSet.as_view({ 'get': 'list' })
exercise_detail = ExerciseViewSet.as_view({ 'get': 'retrieve' })

emails_list = ExerciseEmailViewSet.as_view({'get': 'list'})
emails_detail = ExerciseEmailViewSet.as_view({'get': 'retrieve'})


urlpatterns = [
    path('<slug:link>/profile', views.profile, name='profile'),
    path('<slug:link>/start/<int:p_id>/', views.start, name='start'),
    path('<slug:link>/', views.index, name='index'),
    url(r'^', include(router.urls)),

    # exercise urls
    url('^detail/(?P<pk>[0-9]+)/$', exercise_detail, name='exercise-detail'),
    url('^list/$', exercise_list, name='exercise-list'),

    # exercise emails urls
    url('^emails/list/$',emails_list, name= 'emails_list'),
    url('^emails/(?P<pk>[0-9]+)/$',emails_detail, name= 'emails_detail'),

    # emails in Thread style
    url('^thread/(?P<pk>[0-9]+)/$', ExerciseEmailThreadViewSet.as_view({'get': 'retrieve'}), name='exercise-thread'),

]
