from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('transcribe/', views.transcribe_audio, name='transcribe')
]
