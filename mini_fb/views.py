# mini_fb/views.py
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import * # import all models
from .forms import * # import forms
from typing import Any
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
import random
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
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
  
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
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
  
class UpdateProfileView(LoginRequiredMixin, UpdateView):
  ''' view to update profile '''
  form_class = UpdateProfileForm
  template_name = 'mini_fb/update_profile_form.html'

  def get_object(self):
      # Get the Profile object to prefill form
      return get_object_or_404(Profile, pk=self.kwargs['pk'])
  
  def get_success_url(self) -> str:
    ''' return the url to redirect to on success '''
    # find the profile identified by the PK from the URL pattern
    profile = Profile.objects.get(pk=self.kwargs['pk'])
    return reverse('show_profile', kwargs={'pk':profile.pk})
  
  def form_valid(self, form):
    ''' this method is called after form is validated, before saving data to database '''

    profile = Profile.objects.get(pk=self.kwargs['pk'])

    # attach this profile to the instance of the status message to set its FK
    form.instance.profile = profile

    # save/update the profile to database
    form.save()
    
    # delegate work to superclass method
    return super().form_valid(form)
  
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
  ''' view for deleting status msg '''
  model = StatusMessage
  template_name = 'mini_fb/delete_status_form.html'

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    # get context data from superclass
    context = super().get_context_data(**kwargs)

     # get the StatusMessage object based on its pk
    status_message = self.get_object()

    # access the related Profile 
    profile = status_message.profile

    # add status
    context['status'] = status_message
    # add profile 
    context['profile'] = profile 
    return context
  
  def get_success_url(self) -> str:
    ''' return the url to redirect to on success '''
    # get the StatusMessage object based on its pk
    status_message = self.get_object()

    # get profile
    profile = status_message.profile
  
    return reverse('show_profile', kwargs={'pk':profile.pk})
  
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
  ''' view for updating status msg '''
  model = StatusMessage
  form_class = UpdateStatusMessageForm
  template_name = 'mini_fb/update_status_form.html'

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    # get context data from superclass
    context = super().get_context_data(**kwargs)

     # get the StatusMessage object based on its pk
    status_message = self.get_object()

    # access the related Profile 
    profile = status_message.profile

    # add status
    context['status'] = status_message
    # add profile 
    context['profile'] = profile 
    return context
  
  def get_success_url(self) -> str:
    ''' return the url to redirect to on success '''
    # get the StatusMessage object based on its pk
    status_message = self.get_object()

    # get profile
    profile = status_message.profile
  
    return reverse('show_profile', kwargs={'pk':profile.pk})

class CreateFriendView(LoginRequiredMixin, View):
  ''' view for creating friends '''

  def dispatch(self, request, *args, **kwargs):
    # get id
    profile1_id = self.kwargs.get('pk')
    profile2_id = self.kwargs.get('other_pk')

    # get the profile objects
    profile1 = get_object_or_404(Profile, id=profile1_id)
    profile2 = get_object_or_404(Profile, id=profile2_id)

    # add friends
    profile1.add_friend(profile2)

    # redirect to profile
    return redirect('show_profile', pk=profile1.pk)

class ShowFriendSuggestionsView(DetailView):
  ''' view for showing friend suggestions '''
  model = Profile
  template_name = 'mini_fb/friend_suggestions.html'
  context_object_name = 'profile'

class ShowNewsFeedView(DetailView):
  ''' view for showing news feed '''
  model = Profile
  template_name = 'mini_fb/news_feed.html'
  context_object_name = 'profile'

class RegistrationView(CreateView):
  ''' handle registration of new users '''
  template_name = "mini_fb/register.html"
  form_class = UserCreationForm

  def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    if self.request.POST:
      # we handle POST
      print(f"RegistrationView.dispath: {self.request.POST}")

      # reconstruct UserCreateForm from the POst data
      form = UserCreationForm(self.request.POST)

      if not form.is_valid:
        # re-display form with errors
        return super().dispatch(request, *args, **kwargs)        

      # sae the form, which creates new 
      user = form.save()

      # log User in
      login(self.request, user)

      # attach FK use rto profile form instance

    # relax, let CreateView.dispatch handle it!
    return super().dispatch(request, *args, **kwargs)