from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='profile')

    def __str__(self):
        return self.user.email
