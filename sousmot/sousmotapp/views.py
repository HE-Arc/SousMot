from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic, View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.http import JsonResponse, HttpResponse

from .models import Game, Dictionary, Mode

import random
import string

from .forms import GuestUsernameForm

# Create your views here.



def index(request):
    context = {}
    return render(request, 'sousmotapp/index.html', context)


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
