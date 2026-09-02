from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(OfferProduct)
admin.site.register(SubCategory)
admin.site.register(Category)

@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['id','name','desc','price']