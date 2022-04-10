from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic, View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from .models import Game, Mode, Dictionary


def index(request):
    context = { 
        'is_guest' : request.user.is_authenticated,
    }
    return render(request, 'sousmotapp/index.html', context)


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

        # TODO: Uncomment
        # if kwargs["slug"] in self.request.session["creator"]:
        #     context["is_host"] = True

        return context
