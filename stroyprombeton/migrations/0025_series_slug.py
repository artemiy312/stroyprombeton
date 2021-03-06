# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-09 11:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stroyprombeton', '0024_fix_series_option_relation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='option',
            options={'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AddField(
            model_name='series',
            name='slug',
            field=models.SlugField(default='', unique=True),
            preserve_default=False,
        ),
    ]
