from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from main.models import Item, Shop, Department
from main.permissions import SuperUser, IsAdminOrReadOnly, IsSuperOrReadOnly
from main.serializers import SuperUserSerializers, StaffSerializers, NamedUserSerializers, UserSerializers, \
    AnonymousSerializer


class ItemViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly, )

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Item.objects.order_by('id')
        else:
            return Item.objects.filter(is_sold=False).order_by('id')

    def get_serializer_class(self):
        if self.request.user.is_anonymous:
            return AnonymousSerializer
        elif self.request.user.is_superuser:
            return SuperUserSerializers.ItemSerializer
        elif self.request.user.is_staff:
            return StaffSerializers.ItemSerializer
        elif self.request.user.first_name and self.request.user.last_name:
            return NamedUserSerializers.ItemSerializer
        else:
            return UserSerializers.ItemSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.order_by('id')
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Department.objects.order_by('id')
        else:
            return Department.objects.filter(items__is_sold=False).distinct().order_by('id')

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return SuperUserSerializers.DepartmentSerializer
        elif self.request.user.is_staff:
            return StaffSerializers.DepartmentSerializer
        elif self.request.user.first_name and self.request.user.last_name:
            return NamedUserSerializers.DepartmentSerializer
        else:
            return UserSerializers.DepartmentSerializer


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.order_by('id')
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Shop.objects.order_by('id')
        else:
            return Shop.objects.filter(departments__items__is_sold=False).distinct().order_by('id')

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return SuperUserSerializers.ShopSerializer
        elif self.request.user.is_staff:
            return StaffSerializers.ShopSerializer
        elif self.request.user.first_name and self.request.user.last_name:
            return NamedUserSerializers.ShopSerializer
        else:
            return UserSerializers.ShopSerializer


@action(methods=['delete'], detail=False, permission_classes=(SuperUser, ))
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSuperOrReadOnly, )
    queryset = User.objects.order_by('id')

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return SuperUserSerializers.UserSerializer
        else:
            return StaffSerializers.UserSerializer


class UnsoldItemsViewSet(viewsets.ModelViewSet):
    permission_classes = (SuperUser, )
    queryset = Item.objects.filter(is_sold=False)
    serializer_class = SuperUserSerializers.ItemSerializer

    def delete(self, request):
        objects = self.queryset
        objects.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
