from django.urls import path, include
from django.contrib import admin
from .views import SignUpView

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', views.index, name='index')
]
