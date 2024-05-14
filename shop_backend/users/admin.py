from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import ShopUser


@admin.register(ShopUser)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'id',
        'username',
        'email'
    )
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')
    list_display_links = ('username',)
