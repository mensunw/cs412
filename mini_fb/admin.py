# blog/admin.py
# tell admin we want to administer these moels

from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Profile)
admin.site.register(StatusMessage)