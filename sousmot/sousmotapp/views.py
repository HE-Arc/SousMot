from django.shortcuts import render
from django.views import View
from django.views import generic
from .models import Game


def index(request):
    context = {}
    return render(request, 'sousmotapp/index.html', context)



class GameView(generic.CreateView):
    model = Game
    fields = ['mode','nb_letters' ,'time_s', 'nb_words']
    template_name = 'sousmotapp/game.html'
