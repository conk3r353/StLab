from rest_framework import serializers
import rest_framework.fields as fields
from django.contrib.auth.models import User

from main.models import Item, Shop, Department


class UnsoldListSerializer(serializers.ListSerializer):
    def delete(self, instance):
        pass


class SuperUserSerializers:
    class ItemSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = Item
            fields = (
                'id', 'name', 'description', 'price',
                'is_sold', 'comments', 'department'
            )

    class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = Department
            fields = ('id', 'sphere', 'staff_amount', 'shop')

    class ShopSerializer(serializers.ModelSerializer):
        class Meta:
            model = Shop
            fields = ('id', 'name', 'address', 'staff_amount')

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'username', 'is_superuser', 'first_name', 'last_name', 'is_staff')

    class UnsoldSerializer(serializers.ModelSerializer):
        class Meta:
            model = Item
            list_serializer_class = UnsoldListSerializer


class StaffSerializers:
    class ItemSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = Item
            fields = (
                'name', 'description', 'price',
                'is_sold', 'comments', 'department'
            )

    class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = Department
            fields = ('sphere', 'staff_amount', 'shop')

    class ShopSerializer(serializers.ModelSerializer):
        class Meta:
            model = Shop
            fields = ('name', 'address', 'staff_amount')

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'username', 'is_superuser', 'first_name', 'last_name', 'is_staff')
            read_only_fields = fields


class NamedUserSerializers:
    class ItemSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = Item
            fields = (
                'id', 'name', 'description', 'price',
                'is_sold', 'comments', 'department'
            )
            read_only_fields = fields

    class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = Department
            fields = ('id', 'sphere', 'staff_amount', 'shop')
            read_only_fields = fields

    class ShopSerializer(serializers.ModelSerializer):
        class Meta:
            model = Shop
            fields = ('id', 'name', 'address', 'staff_amount')
            read_only_fields = fields


class UserSerializers:
    class ItemSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = Item
            fields = (
                'id', 'name', 'description',
                'is_sold', 'comments', 'department'
            )
            read_only_fields = fields

    class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = Department
            fields = ('id', 'sphere', 'shop')
            read_only_fields = fields

    class ShopSerializer(serializers.ModelSerializer):
        class Meta:
            model = Shop
            fields = ('id', 'name', 'address')
            read_only_fields = fields


class AnonymousSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('name', 'description')
        read_only_fields = fields
