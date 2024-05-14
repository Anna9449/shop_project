from http import HTTPStatus

from django.db.models import F, Sum
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response

from .filters import ProductFilter
from .serializers import (CategorySerializer, ProductSerializer,
                          ShoppingCartSerializer, SubcategorySerializer,
                          TotalShoppingCartSerializer)
from products.models import Category, Product, ShoppingCart, Subcategory


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.prefetch_related('subcategories')
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class SubcategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubcategorySerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Subcategory.objects.select_related('category').filter(
            category__slug=self.kwargs.get('categories_slug')
        )


class ProductViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    http_method_names = ('get', 'post')
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('name',)
    filterset_class = ProductFilter

    def get_permissions(self):
        if self.action == 'add_product_in_cart':
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'add_product_in_cart':
            return ShoppingCartSerializer
        return ProductSerializer

    def get_queryset(self):
        return Product.objects.select_related(
            'subcategory', 'subcategory__category').prefetch_related('images')

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed('POST')

    @action(['POST'], detail=True, url_path='add_product_in_cart')
    def add_product_in_cart(self, request, pk):
        product = get_object_or_404(self.get_queryset(), pk=pk)
        product_in_cart = ShoppingCart.objects.filter(
            user=request.user.id, product=product.id
        )
        if not product_in_cart.exists():
            serializer = self.get_serializer(
                data={'user': request.user.id,
                      'product': product.id},
                context=self.get_serializer_context()
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.CREATED)
        return Response(status=HTTPStatus.BAD_REQUEST)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    pagination_class = None
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ('get', 'patch', 'delete')

    def get_serializer_class(self):
        if self.action == 'total_shopping_cart':
            return TotalShoppingCartSerializer
        return ShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.select_related('user', 'product').filter(
            user=self.request.user
        )

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'queryset': self.get_queryset()
        }

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PATCH')

    @action(['GET'], detail=False, url_path='total_shopping_cart')
    def total_shopping_cart(self, request):
        total_price = self.get_queryset().annotate(
            total_price=F('amount_product') * F('product__price')
        ).aggregate(Sum('total_price'))
        total_amount = self.get_queryset().aggregate(Sum('amount_product'))
        serializer = TotalShoppingCartSerializer(
            data={
                'total_amount': total_amount['amount_product__sum'],
                'total_price': total_price['total_price__sum']
            },
            context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=HTTPStatus.OK)

    def change_amount_product(self, product, amount_product):
        serializer = self.get_serializer(
            product,
            data={'amount_product': amount_product},
            context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTPStatus.OK)

    @action(['PATCH'], detail=True, url_path='increase_amount_product')
    def increase_amount_product(self, request, pk):
        product = get_object_or_404(self.get_queryset(), pk=pk)
        return self.change_amount_product(product, product.amount_product+1)

    @action(['PATCH'], detail=True, url_path='reduce_amount_product')
    def reduce_amount_product(self, request, pk):
        product = get_object_or_404(self.get_queryset(), pk=pk)
        if product.amount_product > 1:
            return self.change_amount_product(
                product, product.amount_product-1
            )
        else:
            product.delete()
            return Response(status=HTTPStatus.NO_CONTENT)

    @action(['DELETE'], detail=False, url_path='delete_shopping_cart')
    def delete_shopping_cart(self, request):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=HTTPStatus.NO_CONTENT)
        return Response(status=HTTPStatus.BAD_REQUEST)
