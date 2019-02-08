from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import object
from django.db import models
ADDRESS_DISPLAY_CHARS = 25


class ZipCode(models.Model):
    zip_code = models.CharField(db_index=True, max_length=10)
    latitude = models.DecimalField(db_index=True, max_digits=10, decimal_places=6)
    longitude = models.DecimalField(db_index=True, max_digits=10, decimal_places=6)
    state = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    country_code = models.CharField(max_length=2, blank=False)

    class Meta(object):
        unique_together = [('zip_code', 'country_code')]

    def __unicode__(self):
        return self.zip_code
