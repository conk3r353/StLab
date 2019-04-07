from django.db import models
from django.contrib.postgres.fields import ArrayField


class Shop(models.Model):
    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return f'Магазин {self.name}'

    def __repr__(self):
        return str(self)

    name = models.CharField(max_length=30, verbose_name='Название магазина')
    address = models.CharField(max_length=150, verbose_name='Адрес магазина', null=True, blank=True)
    staff_amount = models.IntegerField(verbose_name='Кол-во сотрудников магазина')


class Department(models.Model):
    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'

    def __str__(self):
        return f'Департамент {self.sphere} - {self.shop}'

    def __repr__(self):
        return str(self)

    sphere = models.CharField(max_length=30, verbose_name='Сфера деятельности')
    staff_amount = models.IntegerField(verbose_name='Кол-во сотрудников департамента')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Магазин', related_name='departments')


class Item(models.Model):
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'Товар {self.name} - {self.price}'

    def __repr__(self):
        return str(self)

    name = models.CharField(max_length=30, verbose_name='Название товара')
    description = models.TextField(verbose_name='Описание товара', null=True, blank=True)
    price = models.FloatField(verbose_name='Цена товара')
    is_sold = models.BooleanField(verbose_name='Товар продан?')
    comments = ArrayField(models.CharField(max_length=50), verbose_name='Комментарии', null=True, blank=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, verbose_name='Департамент', related_name='items'
    )


class Statistics(models.Model):
    def __str__(self):
        return f'Статистика по {self.url}'

    def __repr__(self):
        return str(self)

    url = models.URLField(verbose_name='Ссылка')
    amount = models.IntegerField(verbose_name='Количество посещений')
