from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic, View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.http import JsonResponse

from .models import Game, Dictionary, Mode

from .forms import GameCreationForm

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

#@method_decorator(csrf_exempt, name="dispatch")
class CreateGameView(View):

    def post(self, request):
        form = GameCreationForm(request.POST)

        if not form.is_valid():
            return redirect('index')

        # Create game in DB
        game_obj = Game.objects.create(
            dictionary_id=Dictionary.objects.get(name=form.data["dictionary"]).pk,
            mode_id=Mode.objects.get(name=form.data["mode"]).pk
        )
        game_obj.save()

        return JsonResponse({
            'status_code': 200,
            'data' : form.data,
            'lol' : form.errors
        })