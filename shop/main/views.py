from django.shortcuts import render
from .models import OfferProduct,Category
# Create your views here.
def index(request):
    offer = OfferProduct.objects.filter(is_available=True)
    category = Category.objects.all()
    context={
        'offer' :offer,
        'category': category

    }
    return render(request,'main/index.html',context)


def cart(request):
    return render(request,'main/cart.html')