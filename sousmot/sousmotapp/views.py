from django.shortcuts import render
from django.views import View


def index(request):
    context = {}
    return render(request, 'sousmotapp/index.html', context)
