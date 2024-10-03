## mini_fb_urls.py
## define the URLS for this app

from django.urls import path
from django.conf import settings
from . import views

# define a list of valid URL patterns
urlpatterns = [
  path(r'', views.ShowAllView.as_view(), name="show_all"), 
]