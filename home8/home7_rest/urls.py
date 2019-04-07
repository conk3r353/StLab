from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from main import views


router = routers.DefaultRouter()
router.register('items', views.ItemViewSet, base_name='items')
router.register('departments', views.DepartmentViewSet)
router.register('shops', views.ShopViewSet)
router.register('users', views.UserViewSet)
router.register('unsold-items', views.UnsoldItemsViewSet, base_name='unsold-items')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
