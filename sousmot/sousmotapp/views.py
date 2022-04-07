from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


# Create your views here.

def index(request):
    context = { 
        'is_guest' : request.user.is_authenticated,
    }
    return render(request, 'sousmotapp/index.html', context)


def rules(request):
    context = {}
    return render(request, 'sousmotapp/rules.html', context)


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(*args, **kwargs)
