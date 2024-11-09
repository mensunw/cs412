## mini_fb_urls.py
## define the URLS for this app

from django.urls import path
from . import views

# define a list of valid URL patterns
urlpatterns = [
  path(r'', views.VotersListView.as_view(), name="voters"), 
]