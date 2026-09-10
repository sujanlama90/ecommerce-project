from django.contrib import admin
from .models import *
from django import forms
from django.utils.html import strip_tags, format_html

# Register your models here.
admin.site.site_header='E-Commerce Management'
admin.site.site_title='Sajilo Cart'
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
    list_display = ['id','name','clean_desc','stock','price','display_image']

    @admin.display(description="Text")
    def clean_desc(self, obj):
        return strip_tags(obj.desc)
    
    inlines = [ProductImageAdmin]
    form = ProductAdminForm
    list_editable =['name']

    def display_image(self,obj):
        if obj.image:
            return format_html('<img src="{}" height="100px" width="100px">',obj.image.url)
    class Media:
        js = ('js/subcategory_filter.js',) 