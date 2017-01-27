from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import Polygon, Point, GEOSException


class AbstractCreatedUpdated(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Layer(AbstractCreatedUpdated):
    profile = models.ForeignKey('profiles.Profile', related_name='layers')
    title = models.CharField(max_length=140)
    description = models.TextField(null=True, blank=True)
    area = models.GeometryField(
        help_text='If a polygon is used nodes of this layer will have to be contained in it.'
                  'If a point is used nodes of this layer can be located anywhere. Lines are not allowed.'
    )

    def clean(self):
        """
        Ensure area is either a Point or a Polygon
        """
        if not isinstance(self.area, (Polygon, Point)):
            raise ValidationError({'area': ['Area can be only of type Polygon or Point. Lines are not allowed']})

    @property
    def center(self):
        # if area is point just return that
        if isinstance(self.area, Point) or self.area is None:
            return self.area
        # otherwise return point_on_surface or centroid
        try:
            # point_on_surface guarantees that the point is within the geometry
            return self.area.point_on_surface
        except GEOSException:
            # fall back on centroid which may not be within the geometry
            # for example, a horseshoe shaped polygon
            return self.area.centroid
