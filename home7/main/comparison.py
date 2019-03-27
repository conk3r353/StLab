from django.db.models import Sum, Count

from main.models import Item
from main.constants import *


def comparison(form, department_1, department_2, context):
    for compare_point in form.cleaned_data['compared_fields']:
        if compare_point == WORKERS_TOTAL:
            amount_1 = department_1.staff_amount
            amount_2 = department_2.staff_amount
            label = WORKERS_TOTAL_LABEL

            # context['compared_fields'].append = [amount_1, amount_2, '']

        elif compare_point == PRICE_SOLD:
            amount_1 = Item.objects.filter(department_id=department_1.id,
                                           is_sold=True).aggregate(Sum('price'))['price__sum']
            amount_2 = Item.objects.filter(department_id=department_2.id,
                                           is_sold=True).aggregate(Sum('price'))['price__sum']
            label = PRICE_SOLD_LABEL

            # context['compared_fields']['price_sold'] = [amount_1, amount_2]

        elif compare_point == PRICE_NOT_SOLD:
            amount_1 = Item.objects.filter(department_id=department_1.id,
                                           is_sold=False).aggregate(Sum('price'))['price__sum']
            amount_2 = Item.objects.filter(department_id=department_2.id,
                                           is_sold=False).aggregate(Sum('price'))['price__sum']
            label = PRICE_NOT_SOLD_LABEL

            # context['compared_fields']['price_not_sold'] = [amount_1, amount_2]

        elif compare_point == PRICE_TOTAL:
            amount_1 = Item.objects.filter(department_id=department_1.id).aggregate(Sum('price'))['price__sum']
            amount_2 = Item.objects.filter(department_id=department_2.id).aggregate(Sum('price'))['price__sum']
            label = PRICE_TOTAL_LABEL

            # context['compared_fields']['price_total'] = [amount_1, amount_2]

        elif compare_point == AMOUNT_SOLD:
            amount_1 = Item.objects.filter(department_id=department_1.id,
                                           is_sold=True).aggregate(Count('id'))['id__count']
            amount_2 = Item.objects.filter(department_id=department_2.id,
                                           is_sold=True).aggregate(Count('id'))['id__count']
            label = AMOUNT_SOLD_LABEL

            # context['compared_fields']['amount_sold'] = [amount_1, amount_2]

        elif compare_point == AMOUNT_NOT_SOLD:
            amount_1 = Item.objects.filter(department_id=department_1.id,
                                           is_sold=False).aggregate(Count('id'))['id__count']
            amount_2 = Item.objects.filter(department_id=department_2.id,
                                           is_sold=False).aggregate(Count('id'))['id__count']
            label = AMOUNT_NOT_SOLD_LABEL

            # context['compared_fields']['amount_not_sold'] = [amount_1, amount_2]

        elif compare_point == AMOUNT_TOTAL:
            amount_1 = Item.objects.filter(department_id=department_1.id).aggregate(Count('id'))['id__count']
            amount_2 = Item.objects.filter(department_id=department_2.id).aggregate(Count('id'))['id__count']
            label = AMOUNT_TOTAL_LABEL

            # context['compared_fields']['amount_total'] = [amount_1, amount_2]

        context['compared_fields'].append((amount_1, amount_2, label))

    return context
