from django.conf import settings
from django.contrib.gis.geos import Point
from django.template.loader import render_to_string
from django.utils import timezone
from celery import group
from econativo.celery import app

fotobosque_bot = settings.FOTOBOSQUE_BOT


@app.task
def update_location_from_message(message):
    from .models import TelegramUser
    update_id = message['update_id']
    message = message['message']  # !!!
    message_from = message['from']
    message_id = message['message_id']
    chat_id = message['chat']['id']
    location = message['location']
    telegram_user, created = TelegramUser.objects.get_or_create(
        tid=message_from['id']
    )
    if created is False and telegram_user.update_id and telegram_user.update_id < update_id:
        # Message is old
        return
    if not telegram_user.first_name:
        telegram_user.first_name = message_from.get('first_name')
    if not telegram_user.last_name:
        telegram_user.last_name = message_from.get('last_name')
    if not telegram_user.username:
        telegram_user.username = message_from.get('username')
    telegram_user.last_location = Point(location['longitude'], location['latitude'])
    telegram_user.last_location_date_time = timezone.now()
    telegram_user.update_id = update_id
    telegram_user.save()
    fotobosque_bot.sendMessage(
        chat_id,
        render_to_string('updated_location.txt', {}),
        reply_to_message_id=message_id
    )


@app.task
def update_locations(telegram_update_id=None):
    if telegram_update_id is None:
        from .models import TelegramUser
        try:
            latest_user = TelegramUser.objects.latest('update_id')
            telegram_update_id = latest_user.update_id + 1
        except TelegramUser.DoesNotExist:
            telegram_update_id = 1
    tasks_group = []
    for message in fotobosque_bot.getUpdates(offset=telegram_update_id):
        msg = message['message']
        if msg.get('location'):
            tasks_group.append(update_location_from_message.s(message))
    if len(tasks_group) > 1:
        group(*tasks_group)()
    elif tasks_group:
        tasks_group[0]()
