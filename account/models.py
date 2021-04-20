from typing import Tuple
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
from PIL import Image
from django.utils.timezone import now
from datetime import datetime


# Create your models here.
class State(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Airport(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name,  password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name,  password, **other_fields)

    def create_user(self, email, user_name, password, **other_fields):

        if not email:
            raise ValueError('You must provide an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField('email address', unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    middle_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    image = models.ImageField(default='default.png',
                              upload_to='profile', blank=True, null=True)
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE)
    objects = CustomAccountManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['user_name', 'airport']

    def __str__(self):
        return self.user_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


""" class Profile(models.Model):
    phone = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(default='default.png',
                              upload_to='profile', blank=True, null=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    airport = models.ForeignKey(
        Airport, on_delete=models.CASCADE, default=1)

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

    # override save method

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path) """


class Equipment(models.Model):
    equipment = models.CharField(max_length=20)

    def __str__(self):
        return self.equipment


class Runway(models.Model):
    runway = models.CharField(max_length=20)
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE)

    def __str__(self):
        return self.runway


class FaultLocation(models.Model):
    location = models.CharField(max_length=50)
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE)

    def __str__(self):
        return self.location


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
