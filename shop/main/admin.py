from django.contrib import admin
from .models import *
from django import forms
# Register your models here.
admin.site.register(OfferProduct)
admin.site.register(SubCategory)
admin.site.register(Category)

# Create your models here.
class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
    class Media:
        js = ('js/subcategory_filter.js',)  # We'll add this JS file next

class ProductImageAdmin(admin.TabularInline):
    model = ImageProduct
    extra =1

@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['id','name','desc','price']
    inlines = [ProductImageAdmin]
    form = ProductAdminForm