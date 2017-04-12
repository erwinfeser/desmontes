from django.db import models


class TelegramUser(models.Model):
    tid = models.IntegerField(help_text='Telegram ID')
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return '%s' % self.tid
