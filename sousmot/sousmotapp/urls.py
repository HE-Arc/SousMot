from django.urls import path
from django.contrib import admin
from .views import GameView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('game/', GameView.as_view(), name='game')
]