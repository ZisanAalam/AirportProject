from typing import Tuple
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from PIL import Image
from django.utils.timezone import now
from datetime import datetime 


# Create your models here.
class Profile(models.Model):
    phone = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=100,blank=True, null=True)
    image = models.ImageField(default='default.png' , upload_to='profile',blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    # Create profile object after user object is created
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            

    post_save.connect(create_profile, sender=User)
    
    def save_profile(sender, instance, created, **kwargs):
        if created == False:
            instance.profile.save()
            
    post_save.connect(save_profile, sender=User)

    #override save method

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img = Image.open(self.image.path)

        if img.height>300 or img.width>300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path) 

class Equipment(models.Model):
    equipment = models.CharField(max_length=20)

    def __str__(self):
        return self.equipment

class Runway(models.Model):
    runway = models.CharField(max_length=20)

    def __str__(self):
        return self.runway

class FaultLocation(models.Model):
    location = models.CharField(max_length=50)
    def __str__(self):
        return self.location
        
class FaultEntry(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    runway = models.ForeignKey(Runway, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=False, auto_now=False)
    end_date = models.DateField( auto_now=False, auto_now_add=False)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)

    location = models.ForeignKey(FaultLocation, on_delete=models.CASCADE)
    
    fault_discription = models.CharField(max_length=255)
    action_taken = models.CharField(max_length=255)

    # start_date_time = models.DateTimeField(auto_now=False,auto_now_add=False,default=datetime.now)
    # end_date_time = models.DateTimeField(auto_now=False,auto_now_add=False,default=datetime.now)
    