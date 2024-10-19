# mini_fb/forms.py

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
  ''' form to create a profile for database  '''

  class Meta:
    ''' associate this html form with Profile data model '''
    model = Profile
    fields = ["first_name", "last_name", "city", "email_address", "profile_image_url"] # fields to include in form

class CreateStatusMessageForm(forms.ModelForm):
  ''' form to create a status message for a profile in database  '''

  class Meta:
    ''' associate this html form with status msg data model '''
    model = StatusMessage
    fields = ["message"] # fields to include in form

class UpdateProfileForm(forms.ModelForm):
  ''' form to update profile '''

  class Meta:
    ''' associate this html form with profile model '''
    model = Profile
    fields = ["city","email_address","profile_image_url"]

class UpdateStatusMessageForm(forms.ModelForm):
  ''' form to update profile '''

  class Meta:
    ''' associate this html form with profile model '''
    model = StatusMessage
    fields = ["message"]