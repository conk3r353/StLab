from django import template
from django.db.models import Sum, Count

from main.models import Item

register = template.Library()


@register.simple_tag(name='test')
def test():
    return '<h1>Success!</h1>'


@register.simple_tag(name="get_leader")
def get_leader(department_1, department_2, choice):
    # print(department_1)
    # print(department_2)
    # print(choice)

    def compare(num_1, num_2):
        if num_1 > num_2:
            return num_1
        elif num_2 > num_1:
            return num_2

    if choice == '1':
        amount_1 = department_1.staff_amount
        amount_2 = department_2.staff_amount
        total = compare(amount_1, amount_2)

    elif choice == '2':
        amount_1 = Item.objects.filter(department_id=department_1.id,
                                       is_sold=True).aggregate(Sum('price'))['price__sum']
        amount_2 = Item.objects.filter(department_id=department_2.id,
                                       is_sold=True).aggregate(Sum('price'))['price__sum']
        total = compare(amount_1, amount_2)

    elif choice == '3':
        amount_1 = Item.objects.filter(department_id=department_1.id,
                                       is_sold=False).aggregate(Sum('price'))['price__sum']
        amount_2 = Item.objects.filter(department_id=department_2.id,
                                       is_sold=False).aggregate(Sum('price'))['price__sum']
        total = compare(amount_1, amount_2)

    elif choice == '4':
        amount_1 = Item.objects.filter(department_id=department_1.id).aggregate(Sum('price'))['price__sum']
        amount_2 = Item.objects.filter(department_id=department_2.id).aggregate(Sum('price'))['price__sum']
        total = compare(amount_1, amount_2)

    elif choice == '5':
        amount_1 = Item.objects.filter(department_id=department_1.id,
                                       is_sold=True).aggregate(Count('id'))['id__count']
        amount_2 = Item.objects.filter(department_id=department_2.id,
                                      is_sold=True).aggregate(Count('id'))['id__count']
        total = compare(amount_1, amount_2)

    elif choice == '6':
        amount_1 = Item.objects.filter(department_id=department_1.id,
                                       is_sold=False).aggregate(Count('id'))['id__count']
        amount_2 = Item.objects.filter(department_id=department_2.id,
                                      is_sold=False).aggregate(Count('id'))['id__count']
        total = compare(amount_1, amount_2)

    elif choice == '7':
        amount_1 = Item.objects.filter(department_id=department_1.id).aggregate(Count('id'))['id__count']
        amount_2 = Item.objects.filter(department_id=department_2.id).aggregate(Count('id'))['id__count']
        total = compare(amount_1, amount_2)

    return {'value_1': amount_1, 'value_2': amount_2, 'result': total}
