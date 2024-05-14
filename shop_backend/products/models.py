from io import BytesIO
from django.core.files import File
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from PIL import Image

from .const import (COUNT_DECIMAL_PLACES, MAX_DIGITS_PRICE, MAX_LENGTH_NAME,
                    MAX_LENGTH_SLUG, MAX_VALUE_AMOUNT_PRODUCT,
                    MIN_VALUE_AMOUNT_PRODUCT, SIZE_MEDIUM_IMG, SIZE_SMALL_IMG,)
from users.models import ShopUser as User


class CategoryModel(models.Model):
    name = models.TextField('Наименование',
                            max_length=MAX_LENGTH_NAME)
    slug = models.SlugField('Слаг',
                            max_length=MAX_LENGTH_SLUG, unique=True)
    image = models.ImageField('Изображение')

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(CategoryModel):

    class Meta(CategoryModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subcategory(CategoryModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='Категория'
    )

    class Meta(CategoryModel.Meta):
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Product(models.Model):
    name = models.CharField('Наименование продукта',
                            max_length=MAX_LENGTH_NAME)
    slug = models.SlugField('Слаг',
                            max_length=MAX_LENGTH_SLUG, unique=True)

    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Подкатегория'
    )
    price = models.DecimalField('Цена',
                                max_digits=MAX_DIGITS_PRICE,
                                decimal_places=COUNT_DECIMAL_PLACES)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('subcategory__name',)

    def __str__(self):
        return self.name


class ImageProduct(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Продукт'
    )
    image = models.ImageField('Изображение продукта')
    image_small = models.ImageField('Изображение продукта s')
    image_medium = models.ImageField('Изображение продукта m')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return self.product.name

    def create_image_small_or_medium(self, size):
        img = Image.open(self.image)
        img.thumbnail(size)
        t_io = BytesIO()
        img.save(t_io, 'JPEG', quality=85)
        return File(t_io, name=self.image.name)

    def save(self, *args, **kwargs):
        self.image_small = self.create_image_small_or_medium(
            size=SIZE_SMALL_IMG
        )
        self.image_medium = self.create_image_small_or_medium(
            size=SIZE_MEDIUM_IMG
        )
        super().save(*args, **kwargs)


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    amount_product = models.PositiveSmallIntegerField(
        'Количество',
        default=1,
        validators=[
            MaxValueValidator(MAX_VALUE_AMOUNT_PRODUCT),
            MinValueValidator(MIN_VALUE_AMOUNT_PRODUCT)
        ],
    )

    class Meta:
        verbose_name = 'Корзина продуктов'
        verbose_name_plural = 'Корзина продуктов'
        default_related_name = 'product_in_cart'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'product'),
                name='unique_user_product',
            ),
        )
