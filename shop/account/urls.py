from django.urls import path
from .views import *
urlpatterns = [
    path('log_in/',log_in.as_view(),name='log_in'),
    path('register/',register.as_view(),name='register'),
    path('log_out/',log_out,name='log_out')
]
