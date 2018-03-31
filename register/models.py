from __future__ import unicode_literals
from django.contrib.auth.models import User
from django import forms
from django.db import models
from django.db.models.signals import post_save
#from register.forms import AdminForm
from django.db.models.signals import *
import os

class subject(models.Model):
    userid = models.ManyToManyField(User)
    name= models.CharField(max_length=200)
        
    def __str__(self):
        return self.name
    

# Create your models here.
from django.conf import settings
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name= models.CharField(max_length=200,blank=True)
    about_yourself= models.TextField( blank=True)
    Education =models.TextField(blank=True)
    Experience =models.TextField(blank=True)
    skills =models.TextField(blank=True)
    Work =models.TextField(blank=True)
    profile_photo = models.FileField( blank=True,default="static/abc1.jpg")#default = os.path.join(settings.STATIC_ROOT,'static','abc1.jpg'),
    resume = models.FileField( blank=True,default="static/abc1.jpg")
    status =models.IntegerField(blank=True,default=0)
    interest1 = models.ManyToManyField(subject)
    
    #default = os.path.join(settings.STATIC_ROOT,'static','abc1.jpg'),
   
                            #)#upload_to='media/')
    #rate=models.IntegerField()
#(max_length=100) #upload_to='media/')

    def __str__(self):
        return self.user.username

    def create_user_profile(sender, instance, created, **kwargs):
       if created:
        full_name=''#instance._full_name
        about_yourself=''#instance._about_yourself
        Education=''#instance._Education
        Experience=''#instance._Experience
        skills=''#instance._skills
        Work=''#instance._Work
        profile_photo=''#instance._profile_photo
        resume=''#instance._resume
        status=0
        #c=instance._rate
        interest1 = subject.objects.get(name="English")
        a=Profile.objects.create(user=instance,full_name=full_name,about_yourself=about_yourself,Education=Education,Experience=Experience,skills=skills)#,rate=c)

    post_save.connect(create_user_profile ,sender=User)



class subcategory(models.Model):
    subid = models.ManyToManyField(subject)
    name= models.CharField(max_length=200)
    
    def __str__(self):
        return self.name


class resource(models.Model):
    catid = models.ManyToManyField(subcategory)
    url_field = models.CharField(max_length=500)
    score = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.url_field


    


