from django_filters import CharFilter, FilterSet

from products.models import Product


class ProductFilter(FilterSet):
    category = CharFilter(field_name='subcategory__category__slug',
                          lookup_expr='iexact')
    subcategory = CharFilter(field_name='subcategory__slug',
                             lookup_expr='iexact')

    class Meta:
        model = Product
        fields = ('category', 'subcategory',)