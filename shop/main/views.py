from django.shortcuts import render
from .models import *
from django.db.models import Count,Prefetch
# Create your views here.
def index(request):
    offer = OfferProduct.objects.filter(is_available=True)
    category = Category.objects.annotate(sub_count=Count('subcategory')).prefetch_related(Prefetch('subcategory_set',\
            queryset=SubCategory.objects.annotate(product_count=Count('product'))))

    subid = request.GET.get('subcategory')
    if subid:
        product = Product.objects.filter(subcategory=subid)
    else:
      product = Product.objects.all()
    context={
        'offer' :offer,
        'category': category,
        "product" : product

    }

    if request.headers.get('HX-Request'):
        return render(request,'main/product.html',context)
    
    return render(request,'main/index.html',context)

def cart(request):
    return render(request,'main/cart.html')

def contact(request):
    return render(request,'main/contact.html')

def about(request):
    return render(request,'main/about.html')