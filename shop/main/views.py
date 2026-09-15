from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import *
from django.db.models import Count,Prefetch
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.
def index(request):
    offer = OfferProduct.objects.filter(is_available=True)
    category = Category.objects.annotate(sub_count=Count('subcategory')).prefetch_related(Prefetch('subcategory_set',\
            queryset=SubCategory.objects.annotate(product_count=Count('product'))))

    subid = request.GET.get('subcategory')
    min = request.GET.get('min')
    max = request.GET.get('max')

    if subid and min and max:
        product = Product.objects.filter(subcategory=subid, price__range =(min,max))
    elif subid:
        product = Product.objects.filter(subcategory=subid)
    else:
      product = Product.objects.all()

    paginator = Paginator(product,6)
    page_n = request.GET.get('page')
    data =paginator.get_page(page_n)
    total = data.paginator.num_pages

    context={
        'offer' :offer,
        'category': category,
        "product" : product,
        'data':data,
        'num':[i+1 for i in range(total)]
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

@login_required(login_url='log_in')
def product_detail(request, id):

    product = get_object_or_404(Product, id=id)

    # Get unique sizes available for this product
    sizes = (
        product.variants
        .values_list('size', flat=True)
        .distinct()
    )

    # Get unique colors available for this product
    colors = (
        product.variants
        .values_list('color', flat=True)
        .distinct()
    )

    context = {
        'product': product,
        'sizes': sizes,
        'colors': colors,
    }

    return render(
        request,
        'main/product_detail.html',
        context
    )
