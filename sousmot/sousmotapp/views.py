import random
import string
import time
from collections import Counter

from django.contrib.auth.forms import UserCreationForm
from django.db.models.functions import Length
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic.base import TemplateView
from django.core.cache import cache

from .forms import GuestUsernameForm, GameStartForm
from .models import Game, Dictionary, Mode
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

    def post(self, request, *args, **kwargs):
        form = GameStartForm(request.POST)
        if form.is_valid():
            game = Game.objects.get(uuid=kwargs["slug"])
            game.mode = Mode.objects.get(name=form.data['game_mode'])
            minutes, seconds = form.data['game_duration'].split(":")
            game.time_s = int(minutes) * 60 + int(seconds)
            game.nb_letters = form.data['word_length']
            game.dictionary_id = form.data['dictionary']
            game.in_game = True
            game.save()

            # Generate words
            number_words = int(game.time_s / 5)
            words = Word.objects.annotate(word_len=Length('word')).filter(dictionary=game.dictionary_id,
                                                                          word_len__exact=game.nb_letters)
            generated_words = random.sample(list(words), number_words)
            upper_generated_words = list(map(lambda x: x.word.upper(), generated_words))

            # Cache save
            cache.set(kwargs["slug"] + '_words', upper_generated_words, 7200)
            cache.set(kwargs["slug"] + '_time', time.time() + game.time_s, 7200)

            list_users = cache.get(kwargs["slug"] + "_users")
            list_users_score = list()
            list_users_score.append((request.session["name"],
                                     random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase,
                                                    k=5), 0))
            for user in list_users:
                list_users_score.append(
                    (user[:-1], random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=5), 0))

            cache.set(kwargs["slug"] + "_users_score", list_users_score, 7200)

            return redirect('game', slug=kwargs["slug"])
        else:
            print(form.errors)
            return redirect('game_lobby', slug=kwargs["slug"])

    def get(self, request, *args, **kwargs):

        game = Game.objects.get(uuid=kwargs["slug"])
        game_mode = game.mode.name
        word_length = game.nb_letters

        if game_mode == 'time-attack':

            context = {
                'mode': game_mode.upper(),
                'rows': range(6),
                'end_time': cache.get(kwargs["slug"] + '_time'),
                'word_length': range(word_length),
                'word_length_js': word_length,
                'word_first_letter': cache.get(kwargs["slug"] + '_words')[0][0]
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
        context = {"username": "", "is_guest": False, "is_host": False, "slug": kwargs["slug"]}

        # Give the user a temporary username for the session
        if self.request.user.is_anonymous:
            if "name" not in self.request.session:
                self.request.session["name"] = "Guest-" + "".join(
                    random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k=5))
        else:
            self.request.session["name"] = self.request.user.username

        context["username"] = self.request.session["name"]

        if self.request.user.is_anonymous:
            context["is_guest"] = True

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


class GameResultView(TemplateView):
    template_name = "sousmotapp/result.html"

    def dispatch(self, request, *args, **kwargs):
        # Check if slug is in DB
        if Game.objects.filter(uuid=kwargs["slug"]).count() == 0:
            raise Http404("Game does not exist")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        score_list = cache.get(kwargs["slug"] + "_users_score")
        context = {
            "score_list": enumerate(score_list),
            "slug": kwargs["slug"]
        }

        return context


class VerificationView(View):
    """
    It's used to verify if the word given is the word to guess
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Check if the current game exist and if it has started
        """
        if Game.objects.filter(uuid=kwargs["slug"]).count() == 0:
            raise Http404("Invalid Game")

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        slug = kwargs["slug"]
        word_to_verify = request.GET.get("word")
        word_to_verify = str(word_to_verify).upper()

        if not word_to_verify:
            return JsonResponse({"error": "Not enough parameter"}, status=400)

        word_to_guess = cache.get(slug + "_words")[0]  # TODO: Change 0 with the current word the user is
        word_to_guess_stat = Counter(word_to_guess)

        if len(word_to_guess) != len(word_to_verify):
            return JsonResponse({"result": "Not the same size"}, status=200)

        if word_to_guess[0] != word_to_verify[0]:
            return JsonResponse({"result": "Must start with the same letter"}, status=200)

        # Check in the database if the word given does exist
        game_dic = Game.objects.filter(uuid=slug).get().dictionary.pk

        if Word.objects.filter(dictionary_id=game_dic, word=word_to_verify).count() == 0:
            return JsonResponse({"result": "Not found in dictionnary"}, status=200)

        result = []

        # This part does the dirty job of checking one by one if the letter is at the right place and so on...

        for i in range(len(word_to_verify)):
            letter_guess = word_to_verify[i]
            letter_right = word_to_guess_stat[i]

            if letter_guess == letter_right:
                word_to_guess_stat[letter_guess] -= 1

        # Check
        for i in range(len(word_to_verify)):
            letter_guess = word_to_verify[i]
            letter_right = word_to_guess[i]

            res = {"letter": letter_guess, "type": "wrong"}

            if letter_guess == letter_right:
                res["type"] = "good_place"
            elif letter_guess in word_to_verify:
                if word_to_guess_stat[letter_guess] > 0:
                    res["type"] = "bad_place"
                    word_to_guess_stat[letter_guess] -= 1

            result.append(res)

        json_data = {"result": result}

        if all(element == "good_place" for element in result):
            json_data["next"] = self._get_next_word()

        return JsonResponse(json_data, status=200)


    def _get_next_word(self):
        """
        Get the next word on the list and returns it
        :return:a dictionary containing the first letter for the next word
        """
        return {"first_letter": ""}