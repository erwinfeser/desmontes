from django.contrib.gis import admin
from .models import (
    Profile,
    Complaint
)


class ComplaintAdmin(admin.GeoModelAdmin):
    model = Complaint
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


admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(Profile, ProfileAdmin)
