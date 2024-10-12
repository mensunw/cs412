## mini_fb_urls.py
## define the URLS for this app

from django.urls import path
from django.conf import settings
from . import views

# define a list of valid URL patterns
urlpatterns = [
  path(r'', views.ShowAllProfilesView.as_view(), name="show_all_profiles"), 
  path('profile/<int:pk>', views.ShowProfilePageView.as_view(), name="show_profile"),
  path('create_profile', views.CreateProfileView.as_view(), name='create_profile'),
  path('profile/<int:pk>/create_status', views.CreateStatusMessageView.as_view(), name="create_status"),
]