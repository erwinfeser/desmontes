from rest_framework_gis import serializers
from apps.layers.models import TelegramPhoto


class LayerSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = TelegramPhoto
        geo_field = 'point'
        fields = [
            'id',
            'telegram_user',
            'photo',
            'caption',
            'telegram_file_id',
            'created',
            'updated',
        ]
