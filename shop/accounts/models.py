from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
# Create your models here.
class CustomUser(AbstractUser):
    phone=models.CharField(max_length=14, blank=True, default='')
    street_address=models.CharField(max_length=200, blank=True, default='')

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='profile')
    profile_picture = CloudinaryField('images')
    dob = models.DateField(null=True)
    bio = models.TextField()
    created_at = models.DateField(auto_now=True)