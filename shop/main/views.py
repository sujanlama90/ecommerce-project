from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from django.db.models import Count,Prefetch
from django.contrib.auth.decorators import login_required
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

@login_required(login_url='log_in')
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        Contact.objects.create(name=name,phone=phone,email=email,subject=subject,message=message)
        messages.success(request,'thank you for connecting with us..')
        redirect('contact')
    return render(request,'main/contact.html')

def about(request):
    return render(request,'main/about.html')