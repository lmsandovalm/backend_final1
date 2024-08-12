from django.db import models
from core import settings
from statistics import mean
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers.user import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=30)  
    last_name = models.CharField(max_length=30)  
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=20, default='usuarios')
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
