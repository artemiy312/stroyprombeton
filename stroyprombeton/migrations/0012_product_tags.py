# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-09-17 14:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stroyprombeton', '0011_add_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='products', to='stroyprombeton.Tag', verbose_name='tags'),
        ),
    ]
