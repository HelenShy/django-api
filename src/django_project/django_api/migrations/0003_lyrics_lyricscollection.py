# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-19 12:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_api', '0002_profilefeeditem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lyrics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=255)),
                ('song_title', models.CharField(max_length=255)),
                ('song_lyrics', models.CharField(max_length=1023)),
            ],
        ),
        migrations.CreateModel(
            name='LyricsCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('lyrics_list', models.ManyToManyField(to='django_api.Lyrics', verbose_name='list of lyrics')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
