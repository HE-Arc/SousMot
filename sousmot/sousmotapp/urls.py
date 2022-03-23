from django.urls import path, include
from django.contrib import admin
from django.views.generic.base import TemplateView
from .views import SignUpView

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]
