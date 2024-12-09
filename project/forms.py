# project/forms.py

from django import forms
from .models import Profile, Prediction, Feedback

class PredictionInputForm(forms.Form):
    '''A custom form for user inputs to generate a prediction'''
    game_name = forms.CharField(max_length=100, required=True)
    tag_line = forms.CharField(max_length=100, required=True)

class CreateFeedbackForm(forms.ModelForm):
  ''' 
    A custom form for users to create feedback
  '''

  class Meta:
    ''' associate this html form with status msg data model '''
    model = Feedback
    fields = ["stars","message"] 

class UpdateFeedbackForm(forms.ModelForm):
  ''' 
    A custom form for updating feedback
  '''

  class Meta:
    ''' associate this html form with status msg data model '''
    model = Feedback
    fields = ["stars","message"] 