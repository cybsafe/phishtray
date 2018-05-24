from django.urls import path

from . import views

app_name = 'exercise'

urlpatterns = [
    path('<slug:link>/profile', views.profile, name='profile'),
    path('<slug:link>/start/<int:p_id>/', views.start, name='start'),
    path('<slug:link>/', views.index, name='index'),
    path('', views.index, name='index'),
]
