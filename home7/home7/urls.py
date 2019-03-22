"""home7 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from main import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ShopView.as_view(), name='shop-select'),
    path('item-update/<int:item_id>', views.ItemUpdateView.as_view(), name='item-update'),
    path('item-delete/<int:pk>', views.ItemDeleteView.as_view(), name='item-delete'),
    path('<int:shop_id>/', views.ShopDetailView.as_view(), name='shop-detail'),
    path('new-item/<int:department_id>', views.ItemCreateView.as_view(), name='new-item'),
    path('department-update/<int:department_id>', views.DepartmentUpdateView.as_view(), name='department-update'),
    path('new-department/<int:shop_id>', views.DepartmentCreateView.as_view(), name='new-department'),
    path('department-delete/<int:pk>', views.DepartmentDeleteView.as_view(), name='department-delete'),
    path('shop/<int:shop_id>', views.ShopInfoView.as_view(), name='shop-info'),
    path('filter/item/<int:number>', views.ItemFilterView.as_view(), name='filter-item'),
    path('filter/shop/<int:number>', views.ShopFilterView.as_view(), name='filter-shop'),
    path('compare-request', views.CompareRequestView.as_view(), name='compare-request'),
    path('test-tag', views.TestTagView.as_view(), name='test-tag'),
]
