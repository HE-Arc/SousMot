from django.urls import path, include
from django.contrib import admin
from .views import GameView
from .views import SignUpView
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("admin/", admin.site.urls),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("game/new/", views.CreateGameView.as_view(), name="game_create"),
    # path("accounts/", include("django.contrib.auth.urls")),
    path("lobby/<slug:slug>/", views.GameLobbyView.as_view(), name="game_lobby"),
    path("game/<slug:slug>/verify/", views.VerificationView.as_view(), name="game_verify"),
    path('game/<slug:slug>/', GameView.as_view(), name='game'),
    path('result/<slug:slug>/', views.GameResultView.as_view(), name='result'),
    path('rules/', views.rules, name='rules')
]

