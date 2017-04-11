from django.contrib.gis import admin
from .models import (
    TelegramPhoto
)


class TelegramPhotoAdmin(admin.GeoModelAdmin):
    model = TelegramPhoto
    list_display = [
        'id',
        'telegram_user',
        'photo',
        'created',
        'updated'
    ]
    list_filter = [
        'created',
        'updated'
    ]
    raw_id_fields = [
        'telegram_user'
    ]


admin.site.register(TelegramPhoto, TelegramPhotoAdmin)
