from django.db import models


class TelegramUser(models.Model):
    tid = models.IntegerField(help_text='Telegram ID')
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
