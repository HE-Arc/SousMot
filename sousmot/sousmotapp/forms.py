from django import forms
from .models import Dictionary


class GameCreationForm(forms.Form):
    mode = forms.ChoiceField(choices=[("Time attack", "Time attack"), ("Rounds", "Rounds")])
    word_length = forms.IntegerField(min_value=6, max_value=10)
    dictionary = forms.ModelChoiceField(queryset=Dictionary.objects.all(),to_field_name='name')
