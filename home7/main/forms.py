from django import forms
from django.core.exceptions import ValidationError
from django.forms import Form, CheckboxSelectMultiple
from main.models import Department


class CompareRequestForm(Form):
    choice_select = [(department.id, department.sphere) for department in Department.objects.all()]
    choice_checkbox = (
        (1, 'Количество сотрудников в отделе'),
        (2, 'Суммарная стоимость проданных товаров'),
        (3, 'Суммарная стоимость не проданных товаров'),
        (4, 'Суммарная стоимость всех товаров'),
        (5, 'Количество проданных товаров'),
        (6, 'Количество не проданных товаров'),
        (7, 'Количество всех товаров')
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
