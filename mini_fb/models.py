# mini_fb/models.py
# Define data objects for blog application
from django.db import models

# Create your models here.

class Profile(models.Model):
  ''' Encapsulate the idea of one Profile '''
  # data attributes of an Article:
  first_name = models.TextField(blank=False)
  last_name = models.TextField(blank=False)
  city = models.TextField(blank=False)
  email_address = models.TextField(blank=False)
  profile_image_url = models.URLField(blank=True)

  def __str__(self):
    ''' Return a string representation of object '''
    return f'{self.first_name} {self.last_name}\'s Profile'

