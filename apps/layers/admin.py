from django.contrib.gis import admin
from .models import (
    TelegramPhoto
)


class TelegramPhotoAdmin(admin.GeoModelAdmin):
    model = TelegramPhoto
    openlayers_url = 'https://cdnjs.cloudflare.com/ajax/libs/openlayers/2.13.1/OpenLayers.js'
    list_select_related = [
        'telegram_user'
    ]
    list_display = [
        'id',
        'telegram_user',
        'file_id',
        'photo',
        'created',
        'updated'
    ]
    list_filter = [
        'created',
        'updated'
    ]
    readonly_fields = [
        'photo_hash'
    ]
    raw_id_fields = [
        'telegram_user'
    ]
    search_fields = [
        'telegram_user__tid',
        'telegram_user__first_name',
        'telegram_user__username',
        'file_id'
    ]


admin.site.register(TelegramPhoto, TelegramPhotoAdmin)
