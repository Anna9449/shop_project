from rest_framework import serializers

from products.const import COUNT_DECIMAL_PLACES, MAX_DIGITS_PRICE
from products.models import (Category, Subcategory, ImageProduct,
                             Product, ShoppingCart)


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageProduct
        fields = ('image', 'image_small', 'image_medium')


class ProductSerializer(serializers.ModelSerializer):
    subcategory = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    category = serializers.SerializerMethodField()
    images = ImageSerializer(many=True)

    class Meta:
        model = Product
        fields = ('name', 'slug', 'category', 'subcategory', 'price', 'images')

    def get_category(self, obj):
        return obj.subcategory.category.name


class SubcategorySerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    products = ProductSerializer(many=True)

    class Meta:
        model = Subcategory
        fields = ('name', 'slug', 'category', 'image', 'products')


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ('name', 'slug', 'subcategories', 'image')


class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    product = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = ShoppingCart
        fields = ('product', 'amount_product', 'user')
        read_only_fields = ('user',)


class TotalShoppingCartSerializer(serializers.Serializer):
    products = serializers.SerializerMethodField()
    total_amount = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=MAX_DIGITS_PRICE,
                                           decimal_places=COUNT_DECIMAL_PLACES)

    def get_products(self, obj):
        return ShoppingCartSerializer(self.context['queryset'], many=True).data
