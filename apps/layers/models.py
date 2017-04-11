from django.contrib.gis.db import models


class AbstractCreatedUpdated(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TelegramPhoto(AbstractCreatedUpdated):
    telegram_user = models.ForeignKey('profiles.TelegramUser', related_name='telegram_photos')
    photo = models.ImageField(upload_to='telegram_photos/%Y/%m/%d')
    photo_hash = models.CharField(editable=False, max_length=255, unique=True)
    point = models.PointField()
    caption = models.TextField(null=True, blank=True)
    file_id = models.CharField(max_length=255)
    message_id = models.CharField(max_length=255)
