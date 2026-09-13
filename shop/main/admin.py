from django.contrib import admin
from django import forms
from django.utils.html import strip_tags, format_html

from .models import (
    Contact,
    OfferProduct,
    Category,
    SubCategory,
    Product,
    ImageProduct,
    ProductVariant
)


admin.site.site_header = "E-Commerce Management"
admin.site.site_title = "Sajilo Cart"


admin.site.register(OfferProduct)
admin.site.register(SubCategory)
admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(ProductVariant)

class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'color', 'stock')
    list_filter = ('size', 'color')
    search_fields = ('product__name', 'color', 'size')


class SubCategorySelect(forms.Select):
    def create_option(
        self,
        name,
        value,
        label,
        selected,
        index,
        subindex=None,
        attrs=None,
    ):
        option = super().create_option(
            name=name,
            value=value,
            label=label,
            selected=selected,
            index=index,
            subindex=subindex,
            attrs=attrs,
        )

        # ModelChoiceIteratorValue has a .value attribute
        try:
            subcategory_id = value.value
        except AttributeError:
            subcategory_id = value

        if subcategory_id:
            try:
                subcategory = SubCategory.objects.get(
                    pk=subcategory_id
                )

                option["attrs"]["data-category"] = str(
                    subcategory.category_id
                )

            except (
                SubCategory.DoesNotExist,
                ValueError,
                TypeError,
            ):
                pass

        return option


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            # Parentheses are important
            "subcategory": SubCategorySelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Keep all subcategories available.
        # JavaScript will filter them based on the selected category.
        self.fields["subcategory"].queryset = (
            SubCategory.objects.select_related("category").all()
        )

    def clean(self):
        cleaned_data = super().clean()

        category = cleaned_data.get("category")
        subcategory = cleaned_data.get("subcategory")

        if (
            category
            and subcategory
            and subcategory.category_id != category.id
        ):
            self.add_error(
                "subcategory",
                "Select a subcategory belonging to the selected category.",
            )

        return cleaned_data

    class Media:
        js = ("js/subcategory_filter.js",)


class ProductImageAdmin(admin.TabularInline):
    model = ImageProduct
    extra = 1


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    form = ProductAdminForm
    inlines = [ProductImageAdmin]

    list_display = [
        "id",
        "name",
        "clean_desc",
        "stock",
        "price",
        "display_image",
    ]

    list_editable = ["name"]

    @admin.display(description="Text")
    def clean_desc(self, obj):
        return strip_tags(obj.desc)

    @admin.display(description="Image")
    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" height="100" width="100" '
                'style="object-fit:cover;border-radius:8px;">',
                obj.image.url,
            )

        return "No Image"
