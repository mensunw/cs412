## project_urls.py
## define the URLS for this app

from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

# define a list of valid URL patterns
urlpatterns = [
  path('', views.home, name="home"), 
  # testing url
  path('predict/', views.ShowAllPredictionsView.as_view(), name="show_all_predictions"),
  # enforces a logged-in user
  path('predict/<int:pk>', views.ShowPredictionView.as_view(), name="show_prediction"),
  
  path('feedback/', views.ShowAllFeedbacksView.as_view(), name="feedbacks"),
  path("about", views.about, name="about"),
  path('graphs', views.GraphListView.as_view(), name="graphs"),

  path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
  path('logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name="logout"),
]