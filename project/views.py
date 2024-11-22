from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import * # import all models

# Create your views here.
def home(request):
    '''
    Handles url request for home page
    '''
    # use this template to render the response
    template_name = 'project/home.html'

    # delegate rendering work to the template
    return render(request, template_name)

def about(request):
    '''
    Handles url request for about page
    '''
    # use this template to render the response
    template_name = 'project/about.html'

    # delegate rendering work to the template
    return render(request, template_name)

class ShowAllPredictionsView(ListView):
  ''' 
  the view to show all predictions 
  '''
  model = Profile
  template_name = "project/predict.html"
  context_object_name = 'profiles'

class ShowAllFeedbacksView(ListView):
  '''
  View to show all feedback for feedback center
  '''
  model = Feedback
  template_name = "project/feedbacks.html"
  context_object_name = 'feedbacks'

class GraphListView(ListView):
  '''
  Display several game graphs on it's own page 
  '''

  template_name = 'project/graphs.html'
  model = Game
  context_object_name = "games"