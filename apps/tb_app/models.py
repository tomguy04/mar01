# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.utils import timezone
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if 'name' in postData:
            if len(postData['name']) < 3:
                errors["name"] = "name must be at least 3 characters"
        if len(postData['username']) < 3:
            errors["username"] = "username must be at least 3 characters"
        if len(postData['password']) < 8:
            errors["password"] = "password must be at least 8 characters"
            
        return errors

class TripManager(models.Manager):
    
    def basic_validator(self, postData):
        # DATE_REGEX = re.compile(r'^[0-9]{4,7}-[0-9]{2,2}-[0-9]{2,2}$')
        # DATE_REGEX = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        errors = {}
        if len(postData['destination']) < 1:
                errors["destination"] = "destination in blank, please add a destination"
        if len(postData['description']) < 1:
            errors["description"] = "description in blank, please add a description"
        if len(postData['TravelDateFrom']) < 1:
            errors["TravelDateFrom"] = "TravelDateFrom is blank, please add TravelDateFrom"
        if len(postData['TravelDateTo']) < 1:
            errors["TravelDateTo"] = "TravelDateTo is blank, please add a TravelDateTo"
        if len(postData['TravelDateTo']) > 0 and len(postData['TravelDateFrom']) > 0:
 
            # if datetime.strptime(postData['TravelDateFrom'], '%Y%m%d') <= datetime.today():
            #     errors["TravelDateFrom"] = "TravelDateFrom must be in the future"
            if postData['TravelDateFrom'] <= str(timezone.now().date()):
                errors["TravelDateFrom"] = "TravelDateFrom must be in the future"
            if postData['TravelDateTo'] <= str(timezone.now().date()):
                errors["TravelDateTo"] = "TravelDateTo must be in the future"
            
            if postData['TravelDateFrom'] >= postData['TravelDateTo']:
                errors["TravelDateFrom"] = "TravelDateFrom must be before TravelDateTo"
            # else:
            #     if postData['TravelDateFrom'] <= str(timezone.now().date()):
            #         errors["TravelDateFrom"] = "TravelDateFrom must be in the future"
            #     if postData['TravelDateTo'] <= str(timezone.now().date()):
            #         errors["TravelDateTo"] = "TravelDateTo must be in the future"

                

        return errors
        # datetime.strptime(my_input_time, '%Y%m%d %h:%m:%s')
        
class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
         return self.name

class TripSchedule(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    TravelDateFrom = models.DateField()
    TravelDateTo = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name = 'users') #added, a user can have many tripscheudles.
    objects = TripManager()
    # user_id = models.IntegerField()
    # objects = TripManager()


#carried over from old code.
# class Follow(models.Model): 
#     trip = models.ForeignKey(TripSchedule, related_name = 'users')
#     follower= models.ForeignKey(User, related_name = 'trips')

class Follow(models.Model): 
    trip = models.ForeignKey(TripSchedule, related_name = 'users')
    follower= models.ForeignKey(User, related_name = 'trips')


# Got rid of this code since the user id is now directly associated with the trip id.
# class Trip(models.Model): #addded
#     # admin = models.ForeignKey(TripSchedule, related_name = "trips")
#     # admin = models.OneToOneField(User, on_delete=models.CASCADE) 
#     admin = models.ForeignKey(User, related_name = 'adminrelated') 
#     trip = models.OneToOneField(TripSchedule, on_delete=models.CASCADE)
    

# class TripUser(models.Model):
#     user = models.ForeignKey(User, related_name = 'trips')
#     trip = models.ForeignKey(TripSchedule, related_name = 'users')
