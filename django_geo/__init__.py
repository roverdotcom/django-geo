from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from past.utils import old_div
from builtins import object
from decimal import Decimal
from .distances import distances

from geopy import Point as GeoPyPoint
from geopy.distance import distance as geopy_distance


class Point(object):
    """
    Two-tuple of lat/lng.
    Stored as Decimal.
    """

    MAX_LATITUDE = Decimal('90.0')
    MIN_LATITUDE = Decimal('-90.0')

    MAX_LONGITUDE = Decimal('180.0')
    MIN_LONGITUDE = Decimal('-180.0')

    def __hash__(self):
        return (hash(self.lat) * 179) ^ hash(self.lng)
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.lat != other.lat:
            return False
        if self.lng != other.lng:
            return False
        return True
    def __ne__(self, other):
        return not (self == other)
    def __init__(self, *args, **kwargs):
        if 'lat' in kwargs and 'lng' in kwargs:
            self.lat = Decimal(str(kwargs.pop('lat')))
            self.lng = Decimal(str(kwargs.pop('lng')))
        elif 'latitude' in kwargs and 'longitude' in kwargs:
            self.lat = Decimal(str(kwargs.pop('latitude')))
            self.lng = Decimal(str(kwargs.pop('longitude')))
        elif len(args) == 2:
            self.lat = Decimal(str(args[0]))
            self.lng = Decimal(str(args[1]))
        else:
            raise Exception("Invalid constructor params to Point")
        if self.lat > self.MAX_LATITUDE or self.lat < self.MIN_LATITUDE:
            raise Exception("Invalid latitude value")
        if self.lng > self.MAX_LONGITUDE or self.lng < self.MIN_LONGITUDE:
            raise Exception("Invalid longitude value")
        super(Point, self).__init__()
    @property
    def latitude(self):
        """
        Alternate accessor to lat.
        """
        return self.lat
    @property
    def longitude(self):
        """
        Alternate accessor to lng.
        """
        return self.lng

class Bounds(object):
    """
    Effectively two-tuple of Point objects.
    Takes args as sw Point and ne Point,
    Also will accept them as sw=Point,
    ne=Point
    """
    def __hash__(self):
        hsh = 0
        hsh = hash(self.sw) * 127
        hsh = hsh ^ hash(self.ne)
        return hsh
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.sw != other.sw:
            return False
        if self.ne != other.ne:
            return False
        return True
    def __ne__(self, other):
        return not (self == other)
    def __init__(self, *args, **kwargs):
        if 'sw' in kwargs and 'ne' in kwargs:
            # sw & ne points provided
            self.sw = kwargs.pop('sw')
            self.ne = kwargs.pop('ne')
        elif len(args) == 2:
            # sw & ne points provided as args
            self.sw = args[0]
            self.ne = args[1]
        elif len(kwargs) == 4:
            # kwargs minlat, minlng, maxlat, maxlng
            self.sw = Point(kwargs.pop('minlat'), kwargs.pop('minlng'))
            self.ne = Point(kwargs.pop('maxlat'), kwargs.pop('maxlng'))
        # make sure sw is more southwesterly
        # empty bounds is valid, so do > not =>
        if (self.sw.lat > self.ne.lat) or (self.sw.lng > self.ne.lng):
            raise Exception("Points are not in (sw, ne) order")
        super(Bounds, self).__init__()

    @classmethod
    def get_bounds(cls, center, distance):
        """
        Returns a Bounds object based on a center point and a distance.
        """

        d = geopy_distance(kilometers=distance)
        point = GeoPyPoint(center.latitude, center.longitude)

        ne = d.destination(point, 45)
        sw = d.destination(point, 225)

        return Bounds(
            sw=Point(Decimal(sw.latitude), Decimal(sw.longitude)),
            ne=Point(Decimal(ne.latitude), Decimal(ne.longitude)))

    @classmethod
    def get_coord_bounds(cls, lat, lng, distance):
        return cls.get_bounds(Point(lat=lat, lng=lng), distance)

    @classmethod
    def get_center_coords(cls, min_lat, min_lng, max_lat, max_lng):
        approx_distance = distances.geographic_distance(
                min_lat, min_lng, max_lat, max_lng,)

        d = geopy_distance(kilometers=approx_distance / 2.0)
        center = d.destination(GeoPyPoint(max_lat, max_lng), 225)

        return (center.latitude, center.longitude,)

    def get_radius(self):
        approx_distance = distances.geographic_distance(
                self.sw.lat, self.sw.lng,
                self.ne.lat, self.ne.lng)
        return old_div(approx_distance, 2)

