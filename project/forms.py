# project/forms.py

from django import forms
from .models import Profile, Prediction

class PredictionInputForm(forms.Form):
    '''A custom form for user inputs to generate a prediction'''
    game_name = forms.CharField(max_length=100, required=True)
    tag_line = forms.CharField(max_length=100, required=True)