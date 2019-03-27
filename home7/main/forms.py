from django import forms
from django.core.exceptions import ValidationError
from django.forms import Form, CheckboxSelectMultiple

from main.models import Department
from main.constants import *


class CompareRequestForm(Form):
    choice_select = [(department.id, department.sphere) for department in Department.objects.all()]
    choice_checkbox = (
        (WORKERS_TOTAL, WORKERS_TOTAL_LABEL),
        (PRICE_SOLD, PRICE_SOLD_LABEL),
        (PRICE_NOT_SOLD, PRICE_NOT_SOLD_LABEL),
        (PRICE_TOTAL, PRICE_TOTAL_LABEL),
        (AMOUNT_SOLD, AMOUNT_SOLD_LABEL),
        (AMOUNT_NOT_SOLD, AMOUNT_NOT_SOLD_LABEL),
        (AMOUNT_TOTAL, AMOUNT_TOTAL_LABEL)
    )

    department_1 = forms.ChoiceField(choices=choice_select, label='Первый департамент')
    department_2 = forms.ChoiceField(choices=choice_select, label='Второй департамент')
    compared_fields = forms.MultipleChoiceField(widget=CheckboxSelectMultiple, choices=choice_checkbox,
                                                label='Категории для сравнения')

    def clean(self):
        department_1 = self.cleaned_data.get('department_1')
        department_2 = self.cleaned_data.get('department_2')

        if department_1 == department_2:
            raise ValidationError('Пожалуйста, выберите разные департаменты.')

        super().clean()
