# -*- coding: utf-8 -*-
# Generated by Django 1.11.6.dev20180514171339 on 2018-05-14 17:36
from __future__ import unicode_literals

from django.db import migrations, models

ADD_COUNTRY_CODE_SQL = """
UPDATE django_geo_zipcode
SET country_code = 
  CASE WHEN zip_code REGEXP '[0-9]{5}'
    THEN 'US'
    ELSE 'CA'
  END;
"""

BLANK_COUNTRY_CODE_SQL = """
UPDATE django_geo_zipcode SET country_code = '';
"""


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
        migrations.RunSQL(
            ADD_COUNTRY_CODE_SQL,
            reverse_sql=BLANK_COUNTRY_CODE_SQL,
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
