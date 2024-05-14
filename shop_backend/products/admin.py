from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from .models import Category, Subcategory, Product, ShoppingCart, ImageProduct


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
    )
    list_filter = ('name', )
    list_display_links = ('name',)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
        'category'
    )
    list_filter = ('name', )
    list_display_links = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
        'subcategory',
        'price',
    )
    list_filter = ('name', )
    list_display_links = ('name',)


@admin.register(ImageProduct)
class ImageProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product'
    )
    fields = ('product', 'image_preview', 'image')
    readonly_fields = ('image_preview',)
    list_filter = ('product', )

    @admin.display(description='Изображение')
    def image_preview(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80" height="60">')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'product',
        'amount_product',
    )
    list_filter = ('user', )


admin.site.unregister(Group)
