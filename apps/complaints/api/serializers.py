from rest_framework_gis import serializers
from apps.complaints.models import Complaint


class ComplaintSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = Complaint
        geo_field = 'point'
        fields = [
            'id',
            'title',
            'description',
            'profile',
            'created',
            'updated',
        ]
