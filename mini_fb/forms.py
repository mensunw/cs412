# mini_fb/forms.py

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
  ''' form to create a profile for database  '''

  class Meta:
    ''' associate this html form with Profile data model '''
    model = Profile
    fields = ["first_name", "last_name", "city", "email_address"] # fields to include in form

class CreateStatusMessageForm(forms.ModelForm):
  ''' form to create a status message for a profile in database  '''

  class Meta:
    ''' associate this html form with Profile data model '''
    model = StatusMessage
    fields = ["message"] # fields to include in form