from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (
    Category,
    Product,
    ProductImage,
    Comment,
    Order,
    OrderProduct,
    ShippingAddress,
    Sticker
)


admin.site.site_header = "ShopVerse | Adminstration"
admin.site.site_title = "ShopVerse"
admin.site.index_title = "Adminstration"
admin.site.login_template = "admin/login.html"


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "get_image")
    list_editable = ("category",)
    list_filter = ("category",)
    list_display_links = ("name",)
    search_fields = ("name", "description", "category__name")
    inlines = [ProductImageInline]

    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description="Picture")
    def get_image(self, obj):
        return mark_safe(f'<img src= "{obj.get_image()}" width="150">')

@admin.register(Category)
class CategroyAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_display_links = ('name', )
    search_fields = ('name', )

    prepopulated_fields = { 
        'slug': ('name',)
    }



admin.site.register([Sticker, Comment, OrderProduct, Order, ShippingAddress])
