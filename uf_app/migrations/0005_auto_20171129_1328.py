# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-29 16:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uf_app', '0004_auto_20171127_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ufvalue',
            name='value',
            field=models.DecimalField(decimal_places=3, max_digits=12, verbose_name='Value in Chilean pesos'),
        ),
    ]
