import hashlib
import requests
from django.core.files.base import ContentFile
from django.db import IntegrityError
from django.core.files import File
from django.conf import settings
from django.template.loader import render_to_string
from celery import group
from econativo.celery import app

fotobosque_bot = settings.FOTOBOSQUE_BOT


@app.task
def create_telegram_photo_from_message(message):
    from .models import TelegramPhoto
    from apps.profiles.models import TelegramUser
    update_id = message['update_id']
    message = message['message']  # !!!
    message_from = message['from']
    message_id = message['message_id']
    chat_id = message['chat']['id']
    telegram_user = TelegramUser.objects.filter(tid=message_from['id']).first()
    if telegram_user is None or telegram_user.last_location is None:
        fotobosque_bot.sendMessage(
            chat_id,
            'La foto fue ignorada porque todavía no compartiste tu ubicación.',
            reply_to_message_id=message_id
        )
        return
    document = message.get('document')
    if document:
        fotobosque_bot.sendMessage(
            chat_id,
            'Por favor, reenviá la foto en forma comprimida en lugar de hacerlo como archivo.',
            reply_to_message_id=message_id
        )
        return
    photo = None
    for selected_photo in message['photo'][::-1]:
        file_size = selected_photo['file_size'] * 10 ** -6
        if file_size < 20.0:
            photo = selected_photo
            break
    if photo is None:
        fotobosque_bot.sendMessage(
            chat_id,
            'La foto tiene un tamaño mayor al que puedo procesar.',
            reply_to_message_id=message_id
        )
        return

    file_id = photo['file_id']
    if TelegramPhoto.objects.filter(file_id=file_id).exists():
        fotobosque_bot.sendMessage(
            chat_id,
            'Tu fotos está duplicada en nuestra base de datos.',
            reply_to_message_id=message_id
        )
        return
    caption = message.get('caption')
    url = settings.TELEGRAM_FILE_ROOT_URL + fotobosque_bot.getFile(file_id)['file_path']
    downloaded = requests.get(url)
    md5 = hashlib.md5(downloaded.content).hexdigest()
    try:
        telegram_photo = TelegramPhoto.objects.create(
            message_id=message_id,
            update_id=update_id,
            caption=caption,
            file_id=file_id,
            telegram_user=telegram_user,
            location=telegram_user.last_location,
            photo=File(ContentFile(downloaded.content), name='%s.jpg' % file_id),
            photo_hash=md5
        )
        longitude, latitude = tuple(telegram_photo.location.coords)
        fotobosque_bot.sendMessage(
            chat_id,
            render_to_string(
                'processed_photo.txt',
                {
                    'location_url': render_to_string(
                        'location_url.txt',
                        {
                            'latitude': latitude,
                            'longitude': longitude,
                        }
                    ),
                    'photo_url': telegram_photo.photo.url,
                    'caption': caption or '-'
                }
            ),
            disable_web_page_preview=True,
            reply_to_message_id=message_id
        )
        return photo
    except IntegrityError:
        fotobosque_bot.sendMessage(
            chat_id,
            'Ocurrió un error al procesar la foto. Probablemente sea una foto duplicada',
            reply_to_message_id=message_id
        )
        return


@app.task
def create_telegram_photos(telegram_update_id=None):
    if telegram_update_id is None:
        from apps.layers.models import TelegramPhoto
        try:
            latest_photo = TelegramPhoto.objects.latest('update_id')
            telegram_update_id = latest_photo.update_id + 1
        except TelegramPhoto.DoesNotExist:
            telegram_update_id = 1
    tasks_group = []
    for message in fotobosque_bot.getUpdates(offset=telegram_update_id):
        msg = message['message']
        if msg.get('photo') or msg.get('document', {}).get('thumb'):
            tasks_group.append(create_telegram_photo_from_message.s(message))
    if len(tasks_group) > 1:
        group(*tasks_group)()
    elif tasks_group:
        tasks_group[0]()
