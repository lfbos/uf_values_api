# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-26 21:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uf_app', '0002_auto_20171126_1431'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ufvalue',
            options={'ordering': ['-date'], 'verbose_name': 'UF value', 'verbose_name_plural': 'UF values'},
        ),
    ]