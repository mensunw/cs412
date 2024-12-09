from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
  ''' Encapsulate the idea of a profile '''
  # every Profile has one User
  user = models.OneToOneField(User, on_delete=models.CASCADE, default=User.objects.get(username="admin").id, related_name="pprofile")
  first_name = models.TextField(blank=False)
  last_name = models.TextField(blank=False)
  game_name = models.TextField(blank=False)
  tag_line = models.TextField(blank=False)
  rank = models.TextField(blank=True)
  email = models.TextField(blank=True)
  profile_image = models.ImageField(blank=True)

  def __str__(self):
    ''' Return a string representation of object '''
    return f'Profile: {self.first_name} {self.last_name}'
  
  def get_predictions(self):
    ''' Return a queryset of all predictions for this profile '''
    # use ORM to retrieve predictions for which the FK is this profile
    predictions = Prediction.objects.filter(profile=self)
    return predictions

class Feedback(models.Model):
  ''' Encapsulate idea of feedback for profiles '''
  profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
  published = models.DateTimeField(auto_now=True)
  message = models.TextField(blank=False)
  stars = models.TextField(blank=False)

  def __str__(self):
    ''' Return a string representation of object '''
    return f'Feedback: {self.message} by {self.profile}'
  
  def get_feedbackResponses(self):
    ''' Return a queryset of all feedback responses for this feedback '''
    # use ORM 
    feedbackResponses = FeedbackResponse.objects.filter(feedback=self)
    return feedbackResponses

class FeedbackResponse(models.Model):
  ''' Encapsulate idea of a response for feedback messages '''
  feedback = models.ForeignKey("Feedback", on_delete=models.CASCADE)
  published = models.DateTimeField(auto_now=True)
  message = models.TextField(blank=False)

  def __str__(self):
    ''' Return a string representation of object '''
    return f'Feedback Response: {self.message}'
  
class Prediction(models.Model):
  ''' Encapsulate idea of a prediction for a profile '''

  profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
  match_id = models.TextField(blank=False)
  outcome = models.TextField(blank=False)
  correct = models.BooleanField(blank=False)
  # NOTE: does NOT connect with Game model

  def __str__(self):
    ''' Return a string representation of object '''
    return f'Prediction for {self.match_id} ({self.profile})'

class Game(models.Model):
  ''' Enacapsulate idea of a game '''
  
  match_id = models.TextField(blank=False)
  # skip timestamp
  gold_ratio = models.FloatField(blank=False)
  xp_ratio = models.FloatField(blank=False)
  cs_ratio = models.FloatField(blank=False)
  kills_ratio = models.FloatField(blank=False)
  win = models.IntegerField(blank=False)

  def __str__(self):
    ''' Return a string representation of object '''
    return f'Game: {self.match_id}'

def load_data():
  ''' 
  loads data into database
  all data has been manually obtained, see here: https://github.com/mensunw/Game_Outcome_Predictor
  '''

  # delete current data in database
  Game.objects.all().delete()

  # open the file for reading:
  filename = 'C:/Users/mensu/Documents/game_data.csv'
  f = open(filename)
  headers = f.readline() # read/discard the headers
  # for each line in file
  for line in f:

    try:
        fields = line.split(',') # create a list of fields

        # create a new instance of Game object with this record from CSV
        voter = Game(match_id=fields[0],
                     gold_ratio=fields[2],
                     xp_ratio=fields[3],
                     cs_ratio=fields[4],
                     kills_ratio=fields[5],
                     win=fields[6]
                    )
        voter.save() # save this instance to the database.
    except Exception as e:
        print(f"Exception on {fields}, {e}")
  print("done")