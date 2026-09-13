from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    phone=models.CharField(max_length=14, blank=True, default='')
    street_address=models.CharField(max_length=200, blank=True, default='')