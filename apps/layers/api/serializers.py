from rest_framework_gis import serializers
from apps.layers.models import TelegramPhoto


class TelegramPhotoSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = TelegramPhoto
        geo_field = 'point'
        fields = [
            'id',
            'telegram_user',
            'photo',
            'caption',
            'created',
            'updated'
        ]
