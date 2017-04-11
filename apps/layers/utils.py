import hashlib
import PIL.Image
import PIL.ExifTags
import requests
import io
from django.core.files.base import ContentFile
from django.core.files import File
from django.conf import settings
from django.contrib.gis.geos import Point
from apps.layers.models import TelegramPhoto
from apps.profiles.models import TelegramUser

telemap_bot = settings.TELEMAP_BOT
get_float = lambda x: float(x[0]) / float(x[1])


def convert_to_degrees(value):
    d = get_float(value[0])
    m = get_float(value[1])
    s = get_float(value[2])
    return d + (m / 60.0) + (s / 3600.0)


def get_lat_lon(info):
    try:
        gps_latitude = info[34853][2]
        gps_latitude_ref = info[34853][1]
        gps_longitude = info[34853][4]
        gps_longitude_ref = info[34853][3]
        lat = convert_to_degrees(gps_latitude)
        if gps_latitude_ref != 'N':
            lat *= -1

        lon = convert_to_degrees(gps_longitude)
        if gps_longitude_ref != 'E':
            lon *= -1
        return lat, lon
    except KeyError:
        return None


def create_telegram_photo_from_message(message):
    message = message['message']
    message_from = message.get('from')
    caption = message.get('caption')
    document = message.get('document')
    message_id = message.get('message_id')

    if document:
        file_id = document['file_id']
        file_name = document['file_name']
        url = settings.TELEGRAM_FILE_ROOT_URL + telemap_bot.getFile(file_id)['file_path']
        downloaded = requests.get(url)
        latitude, longitude = get_lat_lon(PIL.Image.open(io.BytesIO(downloaded.content))._getexif())
        md5 = hashlib.md5(downloaded.content).hexdigest()
        telegram_user, created = TelegramUser.objects.get_or_create(
            tid=message_from['id']
        )
        if created:
            telegram_user.first_name = message_from['first_name']
            telegram_user.username = message_from['username']
            telegram_user.save()
        return TelegramPhoto.objects.create(
            message_id=message_id,
            caption=caption,
            file_id=file_id,
            telegram_user=TelegramUser.objects.get_or_create(
                tid=message_from['id']
            )[0],
            point=Point(longitude, latitude),
            photo=File(
                ContentFile(downloaded.content),
                name=file_name
            ),
            photo_hash=md5
        )


def create_telegram_photos(telegram_update_id=None):
    for message in telemap_bot.getUpdates(offset=telegram_update_id):
        create_telegram_photo_from_message(message)
