from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Item, Shop, Department
from main.permissions import SuperUser, IsAdminOrReadOnly, IsSuperOrReadOnly
from main.serializers import ItemSerializer, DepartmentSerializer, ShopSerializer, UserSerializer


class ItemViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly, )
    serializer_class = ItemSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Item.objects.order_by('id')
        else:
            return Item.objects.filter(is_sold=False).order_by('id')

    def get_serializer(self, *args, **kwargs):
        user = self.request.user
        if user.is_anonymous:
            kwargs['fields_to_leave'] = ['name', 'description']
        elif user.is_staff:
            kwargs['fields_to_leave'] = ['name', 'description', 'price', 'is_sold', 'comments', 'department']
        elif not user.first_name or not user.last_name:
            kwargs['fields_to_leave'] = ['id', 'name', 'description', 'is_sold', 'comments', 'department']
        kwargs['context'] = {'request': self.request}
        return self.get_serializer_class()(*args, **kwargs)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.order_by('id')
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated)
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Department.objects.order_by('id')
        else:
            return Department.objects.filter(items__is_sold=False).distinct().order_by('id')

    def get_serializer(self, *args, **kwargs):
        user = self.request.user
        if user.is_staff:
            kwargs['fields_to_leave'] = ['sphere', 'staff_amount', 'shop']
        elif not user.first_name or not user.last_name:
            kwargs['fields_to_leave'] = ['id', 'name', 'description', 'is_sold', 'comments', 'department']
        kwargs['context'] = {'request': self.request}
        return self.get_serializer_class()(*args, **kwargs)


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.order_by('id')
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated)
    serializer_class = ShopSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Shop.objects.order_by('id')
        else:
            return Shop.objects.filter(departments__items__is_sold=False).distinct().order_by('id')

    def get_serializer(self, *args, **kwargs):
        user = self.request.user
        if user.is_staff:
            kwargs['fields_to_leave'] = ['name', 'address', 'staff_amount']
        elif not user.first_name or not user.last_name:
            kwargs['fields_to_leave'] = ['id', 'name', 'address']
        kwargs['context'] = {'request': self.request}
        return self.get_serializer_class()(*args, **kwargs)


@action(methods=['delete'], detail=False, permission_classes=(SuperUser, ))
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSuperOrReadOnly, )
    queryset = User.objects.order_by('id')
    serializer_class = UserSerializer


class UnsoldItemsViewSet(viewsets.ModelViewSet):
    permission_classes = (SuperUser, )
    queryset = Item.objects.filter(is_sold=False)
    serializer_class = ItemSerializer

    def delete(self, request):
        objects = self.queryset
        objects.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
