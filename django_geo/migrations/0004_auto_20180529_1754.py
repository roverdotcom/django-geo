# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-29 17:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_geo', '0003_auto_20180514_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zipcode',
            name='city',
            field=models.CharField(max_length=150),
        ),
    ]
