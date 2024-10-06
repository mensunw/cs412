# mini_fb/views.py
from django.shortcuts import render
from django.views.generic import ListView
from .models import * # import all models
# Create your views here.

# class-based view
class ShowAllProfilesView(ListView):
  ''' the view to show all Profiles '''
  model = Profile # model to display
  template_name = 'mini_fb/show_all_profiles.html'
  context_object_name = 'profiles' # context variable to use