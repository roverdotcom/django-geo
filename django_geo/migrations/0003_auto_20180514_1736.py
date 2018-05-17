# -*- coding: utf-8 -*-
# Generated by Django 1.11.6.dev20180514171339 on 2018-05-14 17:36
from __future__ import unicode_literals

from django.db import migrations, models


def set_country_codes(apps, schema_editor):
    # Set country_code on ZipCode objects in batches
    # (so as not to read/update 1M rows)
    batch_size = 1000
    if schema_editor.connection.alias == 'default':
        ZipCode = apps.get_model('django_geo', 'ZipCode')
        offset = 0
        while True:
            ids = ZipCode.objects.order_by('id').values_list('id', flat=True)[offset:offset+batch_size]
            if not ids.exists():
                break

            ZipCode.objects.filter(id__in=list(ids)).update(
                country_code=models.Case(
                    models.When(zip_code__regex='[0-9]{5}',
                                then=models.Value('US')),
                    default=models.Value('CA')
                )
            )
            offset += batch_size


def blank_country_codes(apps, *args):
    ZipCode = apps.get_model('django_geo', 'ZipCode')
    ZipCode.objects.all().update(country_code='')


class Migration(migrations.Migration):

    dependencies = [
        ('django_geo', '0002_auto_20180502_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='zipcode',
            name='country_code',
            field=models.CharField(blank=True, default=b'', max_length=2),
        ),
        migrations.RunPython(
            set_country_codes,
            blank_country_codes,
        ),
        migrations.AlterUniqueTogether(
            name='zipcode',
            unique_together=set([('zip_code', 'country_code')]),
        ),
        migrations.AlterField(
            model_name='zipcode',
            name='country_code',
            field=models.CharField(max_length=2),
        ),
    ]
