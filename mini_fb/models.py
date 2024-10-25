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

  def get_friends(self):
    ''' returns a profile's friends '''
    # use ORM to retrieve friends for which the FK is this profile
    friends1 = Friend.objects.filter(profile1=self)
    friends2 = Friend.objects.filter(profile2=self)

    # return profile of friends
    all_friends = []
    for friend in friends1:
      all_friends += [friend.profile2]
    for friend in friends2:
      all_friends += [friend.profile1]

    return all_friends
  
  def add_friend(self, other):
    ''' allows a user to become friends with another user '''

    # check if friend already exists
    our_friends = self.get_friends()
    
    already_friends = False
    for friend in our_friends:
      if friend == other:
        already_friends = True
    
    # check for "self friending"
    if self == other:
      already_friends = True

    # create friend
    if already_friends == False:
      Friend.objects.create(profile1=self, profile2=other)
  
  def get_friend_suggestions(self):
    ''' returns list of possible friends for the profile '''

    # invalid friends (self, friends already with)
    invalid_profiles = self.get_friends()
    invalid_profiles += [self]

    # get all possible friends
    possible_profiles = []
    all_profiles = Profile.objects.all()
    for profile in all_profiles:
      if not (profile in invalid_profiles):
        possible_profiles += [profile]

    # get 5 suggestions or until no more possible profiles
    suggestions = []
    numSuggestions = 0
    while numSuggestions < 5 and numSuggestions < len(possible_profiles):
      suggestions += [possible_profiles[numSuggestions]]
      numSuggestions += 1
    return suggestions


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
  
class Friend(models.Model):
  ''' Encapsulate idea of friends '''

  # 1 to 1 relationship with Profiles
  profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile1")
  profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile2")
  timestamp = models.DateTimeField(auto_now=True)

  def __str__(self):
    ''' Return a string representation of object '''
    return f'{self.profile1.first_name} & {self.profile2.first_name}'