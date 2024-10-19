# mini_fb/views.py
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from .models import * # import all models
from .forms import * # import forms
from typing import Any
# Create your views here.


# class-based view
class ShowAllProfilesView(ListView):
  ''' the view to show all Profiles '''
  model = Profile # model to display
  template_name = 'mini_fb/show_all_profiles.html'
  context_object_name = 'profiles' # context variable to use

class ShowProfilePageView(DetailView):
  ''' the view to show one profile by PK '''
  model = Profile
  template_name = "mini_fb/show_profile.html"
  context_object_name = 'profile'

class CreateProfileView(CreateView):
  ''' the view to create a profile 
  on GET: send back form to display
  on POST: read/process form, save new profile to database 
  '''
  form_class = CreateProfileForm
  template_name = 'mini_fb/create_profile_form.html'

  def get_success_url(self):
    ''' return the url to redirect to on success '''
    # find the profile identified by the PK from the URL pattern
    return reverse('show_profile', kwargs={'pk':self.object.pk})

  
  def form_valid(self, form):
    ''' this method is called after form is validated, before saving data to database '''
    print(f'CreateProfileView.form_valid() form={form.cleaned_data}')
    print(f'CreateProfileView.form_valid(): self.kwargs={self.kwargs}')
    
    # delegate work to superclass method
    return super().form_valid(form)
  
class CreateStatusMessageView(CreateView):
  ''' the view to create a status message
  on GET: send back form to display
  on POST: read/process form, save new profile to database 
  '''
  form_class = CreateStatusMessageForm
  template_name = 'mini_fb/create_status_form.html'

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    # get context data from superclass
    context = super().get_context_data(**kwargs)

    # get pk
    profile = Profile.objects.get(pk=self.kwargs['pk'])

    # add profile referred to by URL into this context
    context['profile'] = profile 
    return context


  def get_success_url(self) -> str:
    ''' return the url to redirect to on success '''
    # find the profile identified by the PK from the URL pattern
    profile = Profile.objects.get(pk=self.kwargs['pk'])
    return reverse('show_profile', kwargs={'pk':profile.pk})
  
  def form_valid(self, form):
    ''' this method is called after form is validated, before saving data to database '''
    print(f'CreateProfileView.form_valid() form={form.cleaned_data}')
    print(f'CreateProfileView.form_valid(): self.kwargs={self.kwargs}')

    profile = Profile.objects.get(pk=self.kwargs['pk'])

    # attach this profile to the instance of the status message to set its FK
    form.instance.profile = profile

    # save the status message to database
    sm = form.save()

    # read the file from the form:
    files = self.request.FILES.getlist('files')

    # for each file create image object and give it its appropiate fields
    for file in files:
      image = Image(status=sm, image_file=file)
      image.save()
    
    # delegate work to superclass method
    return super().form_valid(form)