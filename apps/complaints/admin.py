from django.contrib.gis import admin
from .models import (
    Profile,
    Complaint
)


class ComplaintAdmin(admin.GeoModelAdmin):
    model = Complaint


admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(Profile)
