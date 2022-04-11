import datetime
import random
import time
from .models import Game
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic, View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.http import JsonResponse, Http404
from .models import Game, Mode, Dictionary, Word
from django.db.models.functions import Length


def index(request):
    context = {
        'is_guest': request.user.is_authenticated,
    }
    return render(request, 'sousmotapp/index.html', context)


def rules(request):
    context = {}
    return render(request, 'sousmotapp/rules.html', context)


class GameView(generic.View):
    template_name = 'sousmotapp/game.html'

    def post(self, request):
        game_mode = request.POST.get('gamemode')
        game_duration = request.POST.get('game_duration')
        word_length = int(request.POST.get('word_length'))
        dictionary_pk = request.POST.get('dictionary')

        if game_mode == 'time-attack':
            seconds = int(game_duration.split(":")[0]) * 60 + int(game_duration.split(":")[1])
            end_time = time.time() + seconds
            number_words = int(seconds / 5)
            words = Word.objects.annotate(word_len=Length('word')).filter(dictionary=dictionary_pk,
                                                                          word_len__exact=word_length)
            generated_words = random.sample(list(words), number_words)
            upper_generated_words = list(map(lambda x: x.word.upper(), generated_words))

            context = {
                'mode': "TIME ATTACK",
                'rows': range(6),
                'end_time': end_time,
                'word_length': range(word_length),
                'word_length_js': word_length,
                'word_first_letter': upper_generated_words[0][0]
            }

            return render(request, 'sousmotapp/game.html', context)
        else:
            raise Http404("Not implemented baby !")


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(*args, **kwargs)


class GameLobbyView(TemplateView):
    template_name = "sousmotapp/lobby.html"

    # TODO: Check if slug is in DB

    def get_context_data(self, **kwargs):
        context = {"username": "", "is_guest": False, "is_host": True}

        if self.request.user.is_anonymous:
            context["username"] = "Guest User"  # TODO: Replace with self.request.session["name"]
            context["is_guest"] = True
        else:
            context["username"] = self.request.user.username

        context["dictionaries"] = Dictionary.objects.all()

        # TODO: Uncomment
        # if kwargs["slug"] in self.request.session["creator"]:
        #     context["is_host"] = True

        return context
