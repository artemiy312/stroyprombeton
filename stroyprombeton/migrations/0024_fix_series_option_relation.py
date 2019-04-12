# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-06 08:15
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stroyprombeton', '0023_series_model'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='series',
        ),
        migrations.AddField(
            model_name='option',
            name='series',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='options', to='stroyprombeton.Series', verbose_name='series'),
        ),
    ]