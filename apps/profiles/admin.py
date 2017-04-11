from django.contrib.gis import admin
from .models import (
    TelegramUser,
)


class TelegramUserAdmin(admin.ModelAdmin):
    model = TelegramUser
    list_display = [
        'id',
        'tid',
        'username',
        'first_name',
    ]
    search_fields = [
        'tid',
        'username',
        'first_name',
    ]


admin.site.register(TelegramUser, TelegramUserAdmin)
