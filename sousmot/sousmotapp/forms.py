from django import forms
from .models import Dictionary


class GameStartForm(forms.Form):
    game_mode = forms.ChoiceField(choices=[("time-attack", "time-attack"), ("rounds", "rounds")])
    game_duration = forms.RegexField(regex="[0-9]{2}:[0-9]{2}")
    word_length = forms.IntegerField(min_value=6, max_value=10)
    dictionary = forms.ModelChoiceField(queryset=Dictionary.objects.all())


class GuestUsernameForm(forms.Form):
    guest_username = forms.CharField(max_length=50, required=True, strip=True)
