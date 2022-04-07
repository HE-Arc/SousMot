import django.contrib.auth.urls
from django.urls import path, include
from django.contrib import admin
from .views import SignUpView
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/",
         auth_views.LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True),
         name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # path("accounts/", include("django.contrib.auth.urls")),
    path('', views.index, name='index'),
    path('rules', views.rules, name='rules')
]
