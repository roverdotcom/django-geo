from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from django.contrib import admin

from .models import ZipCode


class ZipCodeAdmin(admin.ModelAdmin):
    list_display = ('zip_code', 'latitude', 'longitude', 'state', 'city')
    list_filter = ('state',)
    search_fields = ('zip_code', 'state', 'city')

admin.site.register(ZipCode, ZipCodeAdmin)
