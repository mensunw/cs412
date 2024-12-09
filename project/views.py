from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.db.models.query import QuerySet
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
  the view to show the prediction screen and one person's prediction history
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
  Changes based on the sorting query from user, default is by recent
  '''
  model = Feedback
  template_name = "project/feedbacks.html"
  context_object_name = 'feedbacks'
  paginate_by = 8

  def get_queryset(self) -> QuerySet[any]:
    '''Limit the results to a small number of records'''

    # default query set is all of the records:
    qs = super().get_queryset()

    # Default sort method
    sort_method = "recent"

    # Change sort method based on input
    if 'sort' in self.request.GET:
      sort_method = self.request.GET['sort']
    
    # sort results by recent
    if sort_method == "recent":
      qs = qs.order_by('-published')
  
    if sort_method == "critical":
      qs = qs.order_by('stars')

    if sort_method == "favorable":
      qs = qs.order_by('-stars')

    return qs
      

class CreateFeedback(CreateView):
  '''
  View to create feedback from a user for a feedback center
  '''
  form_class = CreateFeedbackForm
  template_name = "project/create_feedback_form.html"

  def get_context_data(self, **kwargs: any) -> dict[str, any]:
    # get context data from superclass
    context = super().get_context_data(**kwargs)

    # get profile
    profile = Profile.objects.get(user=self.request.user)

    # add profile referred to by URL into this context
    context['profile'] = profile 
    return context


  def get_success_url(self) -> str:
    ''' 
    return the url to redirect to on success 
    '''
    # find the profile identified by the PK from the URL pattern
    profile = Profile.objects.get(user=self.request.user)
    return reverse('feedbacks')
  
  def form_valid(self, form):
    ''' this method is called after form is validated, before saving data to database '''

    profile = Profile.objects.get(user=self.request.user)

    # attach this profile to the instance of the status message to set its FK
    form.instance.profile = profile

    # save the feedback to database
    form.save()
    
    # delegate work to superclass method
    return super().form_valid(form)

class UpdateFeedbackView(UpdateView):
  ''' view for updating feedback '''
  model = Feedback
  form_class = UpdateFeedbackForm
  template_name = 'project/update_feedback_form.html'

  def get_context_data(self, **kwargs: any) -> dict[str, any]:
    # get context data from superclass
    context = super().get_context_data(**kwargs)

    # get the feedback object based on its pk
    feedback = self.get_object()

    # access the related Profile 
    profile = feedback.profile

    # add status
    context['feedback'] = feedback
    # add profile 
    context['profile'] = profile 
    return context
  
  def get_success_url(self) -> str:
    ''' return the url to redirect to on success '''
    return reverse('feedbacks')

class GraphListView(ListView):
  '''
  Display several game graphs on it's own page 
  '''

  template_name = 'project/graphs.html'
  model = Game
  context_object_name = "games"

  def get_queryset(self) -> QuerySet[any]:
    '''Limit the results based on the filter'''

    # default query set is all of the records:
    qs = super().get_queryset()

    if 'outcome' in self.request.GET:
      # filter results by either only wins or loss
      outcome = self.request.GET['outcome']
      if outcome != "BOTH":
        numerical_outcome = 0
        if outcome == "WIN":
          numerical_outcome = 1
        qs = qs.filter(win=numerical_outcome)
    return qs

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

    # Use filtered QS for these histograms
    filtered_qs = 0
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
  
class DeletePredictionView(DeleteView):
  ''' view for deleting prediction '''
  model = Prediction
  template_name = 'project/delete_prediction_form.html'

  def get_context_data(self, **kwargs: any) -> dict[str, any]:
    # get context data from superclass
    context = super().get_context_data(**kwargs)

    # get the prediction object based on its pk
    prediction = self.get_object()

    # access the related Profile 
    profile = prediction.profile

    # add status
    context['prediction'] = prediction
    # add profile 
    context['profile'] = profile 
    return context

  def get_success_url(self) -> str:
    ''' return the url to redirect to on success '''
    # get the prediction object based on its pk
    prediction = self.get_object()

    # get profile
    profile = prediction.profile
  
    return reverse('show_prediction', kwargs={'pk':profile.pk})