from django.contrib.gis.db import models
from django.conf import settings


class AbstractCreatedUpdated(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='profile')


class Complaint(AbstractCreatedUpdated):
    profile = models.ForeignKey('Profile', related_name='complaints')
    title = models.CharField(max_length=140)
    description = models.TextField(null=True, blank=True)
    point = models.PointField()
