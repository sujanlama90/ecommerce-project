from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import *
from django.db.models import Count,Prefetch,Avg
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .form import ReviewForm
from cart.cart import Cart
import hashlib
import uuid
import base64
import json
import hmac
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
    reviews = product.reviews.all()
    av = reviews.aggregate(avg_rating=Avg('rating'))    # Get unique sizes available for this product
    related_product =Product.objects.filter(category=product.category).exclude(id=product.id)
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

    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('product_detail',id=product.id)

    context = {
        'product': product,
        'sizes': sizes,
        'colors': colors,
        'form':form,
        'reviews':reviews,
        'range':range(1,6),
        'av': round(av['avg_rating'], 1) if av['avg_rating'] is not None else 0,
        'related_product':related_product
    }

    return render(
        request,
        'main/product_detail.html',
        context
    )


'''=======================================================================================================
                                  ADD TO CART

============================================================================================================
'''
def generate_signature(data, secret):
    # signed_field_names must be included in the payload
    signed_fields = data["signed_field_names"].split(",")
    # Create message string in exact order
    message = ",".join([f"{field}={data[field]}" for field in signed_fields])
    signature = hmac.new(
        secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256 #secure data with same fix length , no reveserd
    ).digest() #bite code

    return base64.b64encode(signature).decode("utf-8")


@login_required(login_url='log_in')
def cart_detail(request):
    cart = request.session.get('cart')
    product_code = "EPAYTEST"
    secret_key = "8gBm/:&EnhH.1/q"
    amount = 0
    for item in cart.values():
        amount += float(item['price'])*item['quantity']
    amount = round(amount,2)
    tax_amount = round(amount*0.13,2)
    total_amount =round( amount + tax_amount,2)
    data = {
        "amount": amount,
        "tax_amount": tax_amount,
        "total_amount": total_amount,
        "transaction_uuid": str(uuid.uuid4()),
        "product_code": 'EPAYTEST',
        "product_service_charge": 0,
        "product_delivery_charge": 0,
        "success_url": "http://127.0.0.1:8000/payments/success_url/",
        "failure_url": "http://127.0.0.1:8000/payments/failure_url/",
        "signed_field_names": "total_amount,transaction_uuid,product_code",
        }

    #algorithm : HMAC , SHA 256 bit
    data['signature'] = generate_signature(data,secret_key)

    return render(request, 'main/cart.html',data)

@login_required(login_url='log_in')
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url='log_in')
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url='log_in')
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url='log_in')
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url='log_in')
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")

