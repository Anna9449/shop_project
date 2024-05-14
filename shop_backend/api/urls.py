from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, ProductViewSet,
                    ShoppingCartViewSet, SubcategoryViewSet)

router = DefaultRouter()

router.register(r'products', ProductViewSet, basename='product')
router.register(r'^categories/(?P<categories_slug>[\w.@+-]+)',
                SubcategoryViewSet, basename='subcategory')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'shopping_cart',
                ShoppingCartViewSet, basename='shopping_cart')
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
