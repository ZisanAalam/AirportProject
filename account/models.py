from typing import Tuple
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save
from PIL import Image
from django.utils.timezone import now
from datetime import datetime


# Create your models here.

class Airport(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name,  password, airport, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name,  password, airport, ** other_fields)

    def create_user(self, email, user_name, password, airport, **other_fields):

        if not email:
            raise ValueError('You must provide an email address')

        email = self.normalize_email(email)
        airport = Airport.objects.get(id=airport)
        user = self.model(email=email, user_name=user_name, airport=airport,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField('email address', unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    middle_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    image = models.ImageField(default='default.png',
                              upload_to='profile', blank=True)
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE)
    objects = CustomAccountManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email', 'airport']

    def __str__(self):
        return self.user_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Runway(models.Model):
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE)
    runway = models.CharField(max_length=20)
    def __str__(self):
        return self.runway

class Equipment(models.Model):
    runway    = models.ForeignKey(Runway,on_delete=models.CASCADE)
    equipment = models.CharField(max_length=20)
    
    def __str__(self):
        return self.equipment

class Make(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Model(models.Model):
    name = models.CharField(max_length=20)
    make = models.ForeignKey(Make, on_delete=models.CASCADE)

    def __str__(self):
        return self.name






class FaultLocation(models.Model):
    location = models.CharField(max_length=50)
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE)

    def __str__(self):
        return self.location

class FaultLocationPart(models.Model):
    name = models.CharField(max_length=50)
    faultlocation = models.ForeignKey(FaultLocation, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class FaultEntry(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    runway = models.ForeignKey(Runway, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=False, auto_now=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)

    location = models.ForeignKey(FaultLocation, on_delete=models.CASCADE)

    fault_discription = models.CharField(max_length=255)
    action_taken = models.CharField(max_length=255)

    # start_date_time = models.DateTimeField(auto_now=False,auto_now_add=False,default=datetime.now)
    # end_date_time = models.DateTimeField(auto_now=False,auto_now_add=False,default=datetime.now)
