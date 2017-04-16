from django.contrib.gis.db import models


class TelegramUser(models.Model):
    tid = models.IntegerField(help_text='Telegram ID')
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    last_location = models.PointField(null=True, blank=True, editable=False)
    last_location_date_time = models.DateTimeField(null=True, blank=True, editable=False)
    update_id = models.IntegerField(unique=True, editable=False)

    def __str__(self):
        return '%s' % self.tid
