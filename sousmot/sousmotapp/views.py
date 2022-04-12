import random
import string
import time

from django.contrib.auth.forms import UserCreationForm
from django.db.models.functions import Length
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic.base import TemplateView

from .forms import GuestUsernameForm
from .models import Game, Dictionary
from .models import Word


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


class CreateGameView(View):

    def post(self, request):

        if request.user.is_anonymous:
            form = GuestUsernameForm(request.POST)

            if not form.is_valid():
                request.session["form_guest_username"] = form.errors
                return redirect('index')

            # Store username in the session
            request.session["name"] = form.data["guest_username"]

        game_code = self._generate_random_code(retry=3)

        # Fuck it, give them a 500 error, they might retry...
        if game_code is None:
            return HttpResponse(status=500)

        # The list of game where the user is the creator is stored in the session.
        # They aren't in the DB because this information is never used outside of the lobby
        # to modify the parameter of the game. So its life is highly temporary.
        if "creator" not in request.session:
            request.session["creator"] = []

        request.session["creator"].append(game_code)
        request.session.modified = True

        game_obj = Game.objects.create(uuid=game_code)
        game_obj.save()

        return redirect('game_lobby', slug=game_code)

    def _generate_random_code(self, retry=3):
        """
        Generate a random 10 characters (lowercase, uppercase and digits) string and check the database if the code has already been attributed.
        :param retry: The number of time the method will retry to find a unique string
        :return: The string generated or None if the method couldn't generate a code given the number of retry
        """
        game_code = "".join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=10))
        if Game.objects.filter(uuid=game_code).count() == 0:
            return game_code

        if retry <= 0:
            return None
        else:
            return self._generate_random_code(retry - 1)


class GameLobbyView(TemplateView):
    template_name = "sousmotapp/lobby.html"

    def dispatch(self, request, *args, **kwargs):
        # Check if slug is in DB
        if Game.objects.filter(uuid=kwargs["slug"]).count() == 0:
            raise Http404("Game does not exist")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {"username": "", "is_guest": False, "is_host": False}

        # Give the user a temporary username for the session
        if "name" not in self.request.session:
            self.request.session["name"] = "Guest-" + "".join(
                random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=5))

        if self.request.user.is_anonymous:
            context["username"] = self.request.session["name"]
            context["is_guest"] = True
        else:
            context["username"] = self.request.user.username

        context["dictionaries"] = Dictionary.objects.all()

        # Simple check to see if the current user is the creator of the game
        if "creator" in self.request.session and kwargs["slug"] in self.request.session["creator"]:
            context["is_host"] = True

        # Keep a list of game the use has joined in case they disconnect in the middle of a party
        if "joined_game" not in self.request.session:
            self.request.session["joined_game"] = []

        self.request.session["joined_game"].append(kwargs["slug"])
        self.request.session.modified = True

        return context
