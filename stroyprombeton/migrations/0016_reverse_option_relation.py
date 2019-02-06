# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-05 12:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stroyprombeton', '0015_create_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name'], 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.RemoveField(
            model_name='product',
            name='options',
        ),
        migrations.AddField(
            model_name='option',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='options', to='stroyprombeton.Product', verbose_name='product'),
        ),
    ]
