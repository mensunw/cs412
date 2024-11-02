## mini_fb_urls.py
## define the URLS for this app

from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

# define a list of valid URL patterns
urlpatterns = [
  path(r'', views.ShowAllProfilesView.as_view(), name="show_all_profiles"), 
  path('profile/<int:pk>', views.ShowProfilePageView.as_view(), name="show_profile"),
  path('create_profile', views.CreateProfileView.as_view(), name='create_profile'),
  path('profile/<int:pk>/create_status', views.CreateStatusMessageView.as_view(), name="create_status"),
  path('profile/<int:pk>/update', views.UpdateProfileView.as_view(), name="update_profile"),
  path('status/<int:pk>/delete', views.DeleteStatusMessageView.as_view(), name="delete_status"),
  path('status/<int:pk>/update', views.UpdateStatusMessageView.as_view(), name="update_status"),
  path('profile/<int:pk>/add_friend/<int:other_pk>', views.CreateFriendView.as_view(), name="create_friend"),
  path('profile/<int:pk>/friend_suggestions', views.ShowFriendSuggestionsView.as_view(), name="suggest_friends"),
  path('profile/<int:pk>/news_feed', views.ShowNewsFeedView.as_view(), name="show_feed"),

  # authenticate urls
  path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'),
  path('logout/', auth_views.LogoutView.as_view(next_page='show_all'), name="logout"),
  path('register/', views.RegistrationView.as_view(), name="register"),
]