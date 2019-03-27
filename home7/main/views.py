from django.db.models import Q, F, Sum, Count
from django.shortcuts import render, redirect
from django import views
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView, FormView

from main.models import Shop, Department, Item
from main.forms import CompareRequestForm
from main.comparison import comparison


class ShopView(views.View):
    def get(self, request, **kwargs):
        shops = Shop.objects.all()
        return render(request, 'index.html', context={'shops': shops})

    def post(self, request, **kwargs):
        shop_id = request.POST.get('shop')
        return redirect('shop-detail', shop_id=shop_id)


class ShopDetailView(views.View):
    def get(self, request, shop_id):
        shop = Shop.objects.filter(id=shop_id).prefetch_related('departments').first()
        return render(request, 'shop_detail.html', context={'shop': shop})


class ItemUpdateView(UpdateView):
    model = Item
    pk_url_kwarg = 'item_id'
    fields = ['name', 'description', 'price', 'is_sold', 'comments', 'department']
    template_name = 'item_update.html'

    def get_success_url(self):
        return reverse_lazy("shop-detail", args=[self.object.department.shop_id])


class ItemDeleteView(DeleteView):
    model = Item

    def get_success_url(self):
        return reverse_lazy("shop-detail", args=[self.object.department.shop_id])


class ItemCreateView(CreateView):
    model = Item
    pk_url_kwarg = 'department_id'
    fields = ['name', 'description', 'price', 'is_sold', 'comments']
    template_name = 'item_create.html'

    def form_valid(self, form):
        self.object = Item(department_id=self.kwargs['department_id'], **form.cleaned_data)
        self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("shop-detail", args=[self.object.department.shop_id])


class DepartmentUpdateView(UpdateView):
    model = Department
    pk_url_kwarg = 'department_id'
    template_name = 'department_update.html'
    fields = ['sphere', 'staff_amount', 'shop']

    def get_success_url(self):
        return reverse_lazy("shop-detail", args=[self.object.shop_id])


class DepartmentCreateView(CreateView):
    model = Department
    fields = ['sphere', 'staff_amount']
    template_name = 'item_create.html'
    pk_url_kwarg = 'shop_id'

    def form_valid(self, form):
        self.object = Department(shop_id=self.kwargs['shop_id'], **form.cleaned_data)
        self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("shop-detail", args=[self.object.shop_id])


class DepartmentDeleteView(DeleteView):
    model = Department
    template_name = 'delete.html'

    def get_success_url(self):
        return reverse_lazy("shop-select")


class ShopInfoView(DetailView):
    model = Shop
    pk_url_kwarg = 'shop_id'
    template_name = 'shop_info.html'


class ItemFilterView(ListView):
    model = Item
    template_name = 'item_filter.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        number = self.kwargs['number']

        if number == 1:
            queryset = queryset.filter(department__shop__name__startswith='К')
        elif number == 2:
            queryset = queryset.filter(price__gt=10, department__staff_amount__lt=50)
        elif number == 3:
            queryset = queryset.filter(Q(price__gt=20) | Q(department__staff_amount__gt=50))
        elif number == 4:
            queryset = queryset.filter(department_id__in=[1, 3, 5, 6])
        elif number == 5:
            queryset = queryset.filter(
                (Q(price__gt=10) & Q(name__icontains='а'))
                | (Q(price__lt=20) & Q(name__icontains='о'))
            )
        elif number == 6:
            queryset = queryset.filter(price=F('department__staff_amount')+10)

        return queryset


class ShopFilterView(ListView):
    model = Shop
    template_name = 'shop_filter.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        number = self.kwargs['number']
        result = None

        if number == 1:
            amount = queryset.aggregate(Sum(F('departments__staff_amount')))['departments__staff_amount__sum']
            queryset = queryset.filter(~Q(staff_amount=amount))

        elif number == 2:
            queryset = queryset.filter(Q(departments__items__price__lt=5)).distinct()

        elif number == 3:
            pass

        elif number == 4:
            queryset = queryset.filter(Q(departments__items__price__lte=10)
                                       | Q(departments__items__name__icontains='а'))
            result = dict()

            for shop in queryset:
                amount = queryset.filter(Q(name=shop.name)).aggregate(Count(F('name')))
                if shop.name not in result:
                    result[shop.name] = amount['name__count']
            queryset = queryset.distinct()

        return {'queryset': queryset, 'result': result}


class CompareRequestView(FormView):
    form_class = CompareRequestForm
    template_name = 'compare_request.html'

    def form_valid(self, form):
        department_1 = Department.objects.get(id=int(form.cleaned_data['department_1']))
        department_2 = Department.objects.get(id=int(form.cleaned_data['department_2']))
        context = {'department_1': department_1, 'department_2': department_2, 'compared_fields': list()}

        return render(
            self.request,
            'compare_result.html',
            context=comparison(form, department_1, department_2, context)
        )

    def form_invalid(self, form):
        return super().form_invalid(form)


class TestTagView(FormView):
    form_class = CompareRequestForm
    template_name = 'compare_request.html'

    def form_valid(self, form):
        department_1 = Department.objects.get(id=int(form.cleaned_data['department_1']))
        department_2 = Department.objects.get(id=int(form.cleaned_data['department_2']))
        context = {'department_1': department_1, 'department_2': department_2, 'compared_fields': set()}

        for compare_point in form.cleaned_data['compared_fields']:
            context['compared_fields'].add(compare_point)

        print(context)

        return render(self.request, 'test_tag.html', context=context)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ZeroItemsView(views.View):
    def get(self, request, **kwargs):
        return render(request, 'panic.html')
