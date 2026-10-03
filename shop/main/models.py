from django.db import models
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField
from django_ckeditor_5.fields import CKEditor5Field
from datetime import timedelta
from accounts.models import CustomUser
from django.utils import timezone

#contact model
class Contact(models.Model):
     name = models.CharField(max_length=200)
     email = models.EmailField()
     phone = models.CharField(max_length=20)
     subject = models.CharField(max_length=200)
     message = models.TextField()

class OfferProduct(models.Model):
    title =models.CharField( max_length=200)
    desc = models.TextField()
    price = models.DecimalField(max_digits=8,decimal_places=2)
    image = CloudinaryField('image')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class FlashSale(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='flash_sales',
    )
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('ends_at',)

    def clean(self):
        if self.starts_at and self.ends_at and self.ends_at <= self.starts_at:
            raise ValidationError({'ends_at': 'End time must be after start time.'})

    def __str__(self):
        return self.title


class Category(models.Model):
    title=models.CharField(max_length=200)
    icon = models.CharField(max_length=200,default='fa fa-solid')
    def __str__(self):
            return self.title
    

class SubCategory(models.Model):
    title=models.CharField(max_length=200)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

class Product(models.Model):
    name=models.CharField(max_length=200)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory=models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    desc=  CKEditor5Field('Text', config_name='extends')
    image = CloudinaryField('image',blank=True,null=True) 
    stock = models.PositiveBigIntegerField()
    mark_price = models.DecimalField(max_digits=8,decimal_places=2)
    discount_percent = models.DecimalField(max_digits=4,decimal_places=2)
    price = models.DecimalField(max_digits=8,decimal_places=2,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
         return self.name

    def save(self,*args, **kwargs):
            self.name = self.name.capitalize()
            self.price = self.mark_price*(1-self.discount_percent/100)
            super().save(*args,**kwargs)

    def is_new(self):
         return self.created_at >= timezone.now() - timedelta(days=4) 
            

class ImageProduct(models.Model):
      image = CloudinaryField('image')
      product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')

class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants'
    )
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=50)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.size} - {self.color}"


class Review(models.Model):
     user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
     product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='reviews')
     rating = models.PositiveSmallIntegerField()
     feedback = models.TextField()
     created_at = models.DateField(auto_now=True)


class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='items')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')