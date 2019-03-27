# Generated by Django 2.1.7 on 2019-03-15 20:09

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Название товара')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание товара')),
                ('price', models.IntegerField(verbose_name='Цена товара')),
                ('is_sold', models.BooleanField(verbose_name='Товар продан?')),
                ('comments', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), size=None, verbose_name='Комментарии')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Товары', to='main.Department', verbose_name='Департамент')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
    ]