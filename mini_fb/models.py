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
  #profile_image_url = models.ImageField(blank=True)

  def __str__(self):
    ''' Return a string representation of object '''
    return f'{self.first_name} {self.last_name}\'s Profile'
  
  def get_status_messages(self):
    ''' return a queryset of all status messages for this profile '''

    # use ORM to retrieve comments for which the FK is this profile
    messages = StatusMessage.objects.filter(profile=self)
    return messages

class StatusMessage(models.Model):
  ''' Encapsulate idea of a statusmessage on a profile '''

  # model the 1 to many relationship with profile
  profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
  published = models.DateTimeField(auto_now=True)
  message = models.TextField(blank=False)

  def __str__(self):
    ''' Return a string representation of object '''
    return f'{self.message}'
  
  def get_images(self):
    ''' return queryset of all images for this status message '''

    # use orm to retrieve the images
    images = Image.objects.filter(status=self)
    return images
  
class Image(models.Model):
  ''' Encapsulate idea of images for status msgs '''

  # model 1 to many relationship with StatusMessage
  status = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)
  image_file = models.ImageField(blank=False)
  published = models.DateTimeField(auto_now=True)
  

