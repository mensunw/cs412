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
  path('predict/prediction/<int:pk>/delete', views.DeletePredictionView.as_view(), name="delete_prediction"),
  
  # feedback center
  path('feedback/', views.ShowAllFeedbacksView.as_view(), name="feedbacks"),
  path('feedback/add', views.CreateFeedback.as_view(), name="create_feedback"),
  path('feedback/<int:pk>/update', views.UpdateFeedbackView.as_view(), name="update_feedback"),

  # about
  path("about", views.about, name="about"),

  # graphs
  path('graphs', views.GraphListView.as_view(), name="graphs"),

  # user authentication
  path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
  path('logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name="logout"),
]