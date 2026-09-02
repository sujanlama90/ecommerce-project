from django.shortcuts import render
from .models import OfferProduct
# Create your views here.
def index(request):
    offer = OfferProduct.objects.filter(is_available=True)
    context={
        'offer' :offer
    }
    return render(request,'main/index.html',context)


def cart(request):
    return render(request,'main/cart.html')