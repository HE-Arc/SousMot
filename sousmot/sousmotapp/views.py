import datetime
import time
from .models import Game
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic, View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.http import JsonResponse, HttpResponse, Http404

from .models import Game, Dictionary, Mode

import random
import string

from .forms import GuestUsernameForm


def index(request):
    context = { 
        'is_guest' : request.user.is_authenticated,
    }
    return render(request, 'sousmotapp/index.html', context)

def rules(request):
    context = {}
    return render(request, 'sousmotapp/rules.html', context)
  

class GameView(generic.TemplateView):
    template_name = 'sousmotapp/game.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['mode'] = "TIME ATTACK"
        context['rows'] = range(6)

        end_time = time.time() + 610  # TODO replace by game duration
        context['end_time'] = end_time

        word_length = 5  # TODO replace by word length
        context['word_length'] = range(word_length)
        context['word_length_js'] = word_length

        context['word_first_letter'] = "P"  # TODO replace by first letter of word

        return context

      
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

            # if "joined_game" not in request.session:
            #     request.session["joined_game"] = ()
            #
            # request.session["joined_game"].push()

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

        game_obj = Game.objects.create(uuid=game_code)
        game_obj.save()

        return redirect('game_lobby', slug=game_code)

        # Create game in DB
        #game_obj = Game.objects.create(
        #    dictionary_id=Dictionary.objects.get(name=form.data["dictionary"]).pk,
        #    mode_id=Mode.objects.get(name=form.data["mode"]).pk
        #)
        #game_obj.save()

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
            return self._generate_random_code(retry-1)


class GameLobbyView(TemplateView):
    template_name = "sousmotapp/lobby.html"

    def dispatch(self, request, *args, **kwargs):
        # Check if slug is in DB
        if Game.objects.filter(uuid=kwargs["slug"]).count() == 0:
            raise Http404("Game does not exist")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {"username": "", "is_guest": False, "is_host": True}

        if self.request.user.is_anonymous:
            context["username"] = "Guest User"  # TODO: Replace with self.request.session["name"]
            context["is_guest"] = True
        else:
            context["username"] = self.request.user.username

        # Simple check to see if the current user is the creator of the game
        if kwargs["slug"] in self.request.session["creator"]:
            context["is_host"] = True

        # Keep a list of game the use has joined in case they disconnect in the middle of a party
        if "joined_game" not in self.request.session:
            self.request.session["joined_game"] = ()

        self.request.session["joined_game"].push(kwargs["slug"])

        return context
