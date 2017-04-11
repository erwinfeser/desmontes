import hashlib
import PIL.Image
import PIL.ExifTags
import requests
import io
from django.core.files.base import ContentFile
from django.db import IntegrityError
from django.core.files import File
from django.conf import settings
from django.contrib.gis.geos import Point
from apps.layers.models import TelegramPhoto
from apps.profiles.models import TelegramUser

fotobosque_bot = settings.FOTOBOSQUE_BOT
get_float = lambda x: float(x[0]) / float(x[1])


def convert_to_degrees(value):
    d = get_float(value[0])
    m = get_float(value[1])
    s = get_float(value[2])
    return d + (m / 60.0) + (s / 3600.0)


def get_lat_lon(info):
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


def create_telegram_photo_from_message(message):
    # TODO: Very ugly code, it is a draft that needs to be improved, even it should use aio
    message = message['message']
    message_from = message['from']
    caption = message.get('caption')
    document = message.get('document')
    message_id = message['message_id']
    chat_id = message['chat']['id']

    if document:
        file_size = document['file_size'] * 10 ** -6
        if file_size < 20.0:
            file_id = document['file_id']
            if not TelegramPhoto.objects.filter(file_id=file_id).exists():
                file_name = document['file_name']
                url = settings.TELEGRAM_FILE_ROOT_URL + fotobosque_bot.getFile(file_id)['file_path']
                downloaded = requests.get(url)
                exif = PIL.Image.open(io.BytesIO(downloaded.content))._getexif()
                if exif:
                    try:
                        latitude, longitude = get_lat_lon(exif)
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
                    except IntegrityError:
                        fotobosque_bot.sendMessage(
                            chat_id,
                            'Ocurrió un error al procesar la foto. Probablemente sea una foto duplicada',
                            reply_to_message_id=message_id
                        )
                    except:
                        fotobosque_bot.sendMessage(
                            chat_id,
                            'Ocurrió un error al leer la geolocalización de la foto. Contactar a erwin@feser.net.ar',
                            reply_to_message_id=message_id
                        )
                else:
                    fotobosque_bot.sendMessage(
                        chat_id,
                        'La foto no contiene metadatos (exif), por lo tanto no se puede obtener la geolocalización.',
                        reply_to_message_id=message_id
                    )
            else:
                fotobosque_bot.sendMessage(
                    chat_id,
                    'Esta foto ya fue procesada.',
                    reply_to_message_id=message_id
                )
        else:
            fotobosque_bot.sendMessage(
                chat_id,
                'La foto no puede superar los 20mb.',
                reply_to_message_id=message_id
            )
    else:
        if message.get('photo'):
            fotobosque_bot.sendMessage(
                chat_id,
                'Las fotos tienen que ser enviadas sin comprimir, como archivo.',
                reply_to_message_id=message_id
            )


def create_telegram_photos(telegram_update_id=None):
    for message in fotobosque_bot.getUpdates(offset=telegram_update_id):
        create_telegram_photo_from_message(message)