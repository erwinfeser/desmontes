from django.contrib.gis import admin
from .models import (
    Layer
)


class LayerAdmin(admin.GeoModelAdmin):
    model = Layer
    list_display = [
        'profile',
        'title',
        'created',
        'updated'
    ]
    list_filter = [
        'created',
        'updated'
    ]
    search_fields = [
        'title',
        'profile__user__first_name',
        'profile__user__last_name',
        'profile__user__email'
    ]
    raw_id_fields = [
        'profile'
    ]


admin.site.register(Layer, LayerAdmin)
