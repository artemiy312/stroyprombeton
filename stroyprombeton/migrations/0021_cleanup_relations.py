# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-23 13:43
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stroyprombeton', '0020_clear_product_and_option'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='option',
            name='is_new_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='tags',
        ),
        migrations.AlterField(
            model_name='option',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='stroyprombeton.Product', verbose_name='product'),
        ),
        migrations.AlterField(
            model_name='option',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='options', to='stroyprombeton.Tag', verbose_name='tags'),
        ),
    ]
