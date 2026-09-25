from django.urls import path
from .views import *

urlpatterns = [
    path('success_url/',success_url,name='success_url'),
    path('failure_url/',failure_url,name='failure_url')
]
