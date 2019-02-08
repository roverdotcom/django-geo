from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from builtins import object
from past.utils import old_div
import math

from geopy.distance import distance


class distances(object):
    @staticmethod
    def geographic_distance(lat1, lng1, lat2, lng2):
        return distance(
            (float(lat1), float(lng1),),
            (float(lat2), float(lng2),)).kilometers

    @staticmethod
    def max_variation_lat(distance):
        max_variation = abs(old_div((180 * distance), (6371.01 * math.pi)))
        return max_variation		

    @staticmethod
    def max_variation_lon(address_latitude, distance):
        top = math.sin(distance / 6371.01)
        bottom = math.cos(old_div((math.pi * address_latitude),180))
        ratio = old_div(top, bottom)
        if -1 > ratio or ratio > 1:
            max_variation = 100
        else:
            max_variation = abs(math.asin(ratio) * (old_div(180, math.pi)))
        return max_variation
