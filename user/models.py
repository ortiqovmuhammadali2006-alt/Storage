from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='users/', null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    brith_data = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    
    