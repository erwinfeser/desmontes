from django.contrib.gis import admin
from .models import (
    Profile,
    Complaint
)


class ComplaintAdmin(admin.GeoModelAdmin):
    model = Complaint


class ProfileAdmin(admin.ModelAdmin):
    model = Profile


admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(Profile, ProfileAdmin)
