from django.urls import path
from .views import *
urlpatterns = [
    path('log_in/',log_in,name='log_in'),
    path('register/',register,name='register')
]
