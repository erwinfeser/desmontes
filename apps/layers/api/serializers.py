from rest_framework_gis import serializers
from apps.layers.models import Layer


class LayerSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = Layer
        geo_field = 'area'
        fields = [
            'id',
            'title',
            'description',
            'profile',
            'created',
            'updated',
        ]
