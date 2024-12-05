from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly import offline
import pandas as pd
from .models import * # import all models
from .forms import * # import all forms

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
  the view to show all predictions.
  this is mainly for testing reasons, only the admin will be able to view this (but for now everyone can access)
  '''
  model = Profile
  template_name = "project/predict_all.html"
  context_object_name = 'profiles'

class ShowPredictionView(View):
  ''' 
  the view to show one prediction
  '''

  template_name = "project/predict.html"

  def get(self, request, pk, *args, **kwargs):
    '''Handle GET requests to show the form and prediction history.'''
    profile = get_object_or_404(Profile, pk=pk)

    # pass this information to the template
    context = {
      'profile': profile,
      'form_state': "unsubmitted",
    }

    return render(request, self.template_name, context)

  def post(self, request, pk, *args, **kwargs):
    '''Handle POST requests to process the form submission.'''
    profile = get_object_or_404(Profile, pk=pk)

    # Make sure form input is correct
    form = PredictionInputForm(request.POST)
    if form.is_valid():
      # Extract data from the form
      game_name = form.cleaned_data.get("game_name")
      tag_line = form.cleaned_data.get("tag_line")

      # Check to see if this ign is participating in a live game

      # Call function to extract features, and call model

      # Create a new prediction 
      Prediction.objects.create(
        profile=profile,
        match_id="NA193873",
        outcome="WIN",
        correct=True,
      )

      # Display success message with updated predictions
      return render(request, self.template_name, {
        'profile': profile,
        'form_state': "submitted_success",
      })

    # Handle invalid form submissions
    return render(request, self.template_name, {
      'profile': profile,
      'form_state': "submitted_failure",
    })


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

  def get_context_data(self, **kwargs):
    # Get the superclass version of context
    context = super().get_context_data(**kwargs)

    # Get the queryset and convert it to a DataFrame
    qs = self.get_queryset()
    data = qs.values('gold_ratio', 'xp_ratio', 'cs_ratio', 'kills_ratio', 'win') 
    df = pd.DataFrame(data)

    # Create a correlation matrix
    corr_matrix = df.corr()

    # Convert correlation matrix to a Plotly heatmap
    heatmap = go.Figure(
      data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='Magma',
        zmin=-1,
        zmax=1,
        colorbar=dict(title="Correlation"),
      )
    )
    heatmap.update_layout(title="Feature Correlation Heatmap")

    # Generate HTML div for the plot and add it to context
    heatmap_div = offline.plot(heatmap, auto_open=False, output_type='div')
    context['heatmap_div'] = heatmap_div

    # Convert query set to DataFrame
    data = pd.DataFrame.from_records(qs.values('gold_ratio', 'xp_ratio', 'cs_ratio', 'kills_ratio', 'win'))

    # Create stacked histograms for each feature
    fig = make_subplots(rows=2, cols=2, subplot_titles=['Gold Ratio', 'XP Ratio', 'CS Ratio', 'Kills Ratio'])
    features = ['gold_ratio', 'xp_ratio', 'cs_ratio', 'kills_ratio']
    row, col = 1, 1

    for feature in features:
      # Separate data by "win" label
      win_1 = data[data['win'] == 1][feature]
      win_0 = data[data['win'] == 0][feature]

      # Add histograms for each label
      fig.add_trace(go.Histogram(x=win_1, nbinsx=20, name=f"{feature} (Win)", marker_color='green', opacity=0.75),
                    row=row, col=col)
      fig.add_trace(go.Histogram(x=win_0, nbinsx=20, name=f"{feature} (Loss)", marker_color='red', opacity=0.75),
                    row=row, col=col)

      # Update subplot layout
      fig.update_xaxes(title_text=feature, row=row, col=col)
      fig.update_yaxes(title_text="Count", row=row, col=col)

      col += 1
      if col > 2:  # Move to the next row
        col = 1
        row += 1

    # Update overall layout
    fig.update_layout(
      title_text="Feature Distributions by Win/Loss",
      height=800,
      width=1000,
      barmode='overlay',  # Stacked histograms
      showlegend=True
    )

    # Generate the graph as HTML and pass it to the template
    distributions_div = go.Figure.to_html(fig, full_html=False)
    context['distributions_div'] = distributions_div
    return context