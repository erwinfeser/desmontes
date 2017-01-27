from django.contrib.gis import admin
from .models import (
    Profile,
)


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = [
        'user',
    ]
    search_fields = [
        'user__first_name',
        'user__last_name',
        'user__email'
    ]
    raw_id_fields = [
        'user'
    ]


admin.site.register(Profile, ProfileAdmin)
