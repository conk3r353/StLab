from django.contrib import admin
from django.contrib.admin import ModelAdmin

from main.models import Shop, Department, Item


class ShopAdmin(ModelAdmin):
    fields = ('name', 'address', 'staff_amount')
    list_display = ('name', 'address', 'staff_amount')


class DepartmentAdmin(ModelAdmin):
    fields = ('sphere', 'staff_amount', 'shop')
    list_display = ('sphere', 'staff_amount', 'shop')


class ItemAdmin(ModelAdmin):
    fields = ('name', 'description', 'price', 'is_sold', 'comments', 'department')
    list_display = ('name', 'description', 'price', 'is_sold', 'comments', 'department')


admin.site.register(Shop, ShopAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Item, ItemAdmin)
