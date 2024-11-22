from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Feedback)
admin.site.register(FeedbackResponse)
admin.site.register(Prediction)
admin.site.register(Game)