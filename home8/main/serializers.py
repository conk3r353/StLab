from rest_framework import serializers
from django.contrib.auth.models import User

from main.models import Item, Shop, Department


class DynamicFieldsModelSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        fields_to_leave = kwargs.pop('fields_to_leave', None)
        super().__init__(*args, **kwargs)

        if fields_to_leave is not None:
            allowed = set(fields_to_leave)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ItemSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Item
        fields = (
            'id', 'name', 'description', 'price',
            'is_sold', 'comments', 'department'
        )


class DepartmentSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'sphere', 'staff_amount', 'shop')


class ShopSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'name', 'address', 'staff_amount')


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_superuser', 'first_name', 'last_name', 'is_staff')
