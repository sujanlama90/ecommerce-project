from django.urls import path
from .views import *
urlpatterns = [
    path('',index,name='index'),
    path('cart',cart,name='cart'),
    path('contact/',contact,name='contact'),
    path('about/',about,name='about'),
    path('product_detail/<int:id>/',product_detail,name='product_detail')
]