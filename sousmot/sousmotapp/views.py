from .models import Game
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

# Create your views here.

def index(request):
    context = {}
    return render(request, 'sousmotapp/index.html', context)


class GameView(generic.TemplateView):
    template_name = 'sousmotapp/game.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mode'] = " TIME ATTACK"
        context['rows'] = range(6)
        context['word_length'] = range(5)
        return context



class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(*args, **kwargs)

