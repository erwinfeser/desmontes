# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-11 15:22
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('photo', models.ImageField(upload_to='telegram_photos/%Y/%m/%d')),
                ('photo_hash', models.CharField(editable=False, max_length=255, unique=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('caption', models.TextField(blank=True, null=True)),
                ('file_id', models.CharField(max_length=255, unique=True)),
                ('message_id', models.CharField(max_length=255, unique=True)),
                ('telegram_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='telegram_photos', to='profiles.TelegramUser')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]