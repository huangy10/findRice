# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Activity.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name=b'\xe6\xb4\xbb\xe5\x8a\xa8\xe5\x90\x8d\xe7\xa7\xb0')),
                ('location', models.CharField(max_length=200, verbose_name=b'\xe6\xb4\xbb\xe5\x8a\xa8\xe5\x9c\xb0\xe7\x82\xb9')),
                ('start_time', models.DateTimeField(verbose_name=b'\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4')),
                ('end_time', models.DateTimeField(verbose_name=b'\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe9\x97\xb4')),
                ('last_length', models.IntegerField(verbose_name=b'\xe6\x8c\x81\xe7\xbb\xad\xe6\x97\xb6\xe9\x97\xb4(min)')),
                ('description', models.TextField(verbose_name=b'\xe6\xb4\xbb\xe5\x8a\xa8\xe7\xae\x80\xe4\xbb\x8b')),
                ('reward', models.FloatField(verbose_name=b'\xe5\xa5\x96\xe5\x8a\xb1\xe9\x87\x91\xe9\xa2\x9d')),
                ('max_attend', models.PositiveIntegerField(verbose_name=b'\xe5\x85\x81\xe8\xae\xb8\xe6\x8a\xa5\xe5\x90\x8d\xe7\x9a\x84\xe6\x9c\x80\xe5\xa4\xa7\xe4\xba\xba\xe6\x95\xb0')),
                ('poster', models.ImageField(upload_to=Activity.models.get_activity_poster_path, verbose_name=b'\xe6\xb5\xb7\xe6\x8a\xa5')),
                ('recommended', models.BooleanField(default=False, verbose_name=b'\xe7\x83\xad\xe9\x97\xa8\xe6\x8e\xa8\xe8\x8d\x90')),
                ('time_limited', models.BooleanField(default=False, verbose_name=b'\xe9\x99\x90\xe6\x97\xb6\xe6\x8a\xa5\xe5\x90\x8d')),
                ('num_limited', models.BooleanField(default=False, verbose_name=b'\xe9\x99\x90\xe9\xa2\x9d\xe6\x8a\xa5\xe5\x90\x8d')),
                ('identified', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe8\xae\xa4\xe8\xaf\x81')),
                ('status', models.IntegerField(choices=[(0, b'\xe5\xb0\x9a\xe6\x9c\xaa\xe5\xbc\x80\xe5\xa7\x8b'), (1, b'\xe5\xb7\xb2\xe7\xbb\x8f\xe5\xbc\x80\xe5\xa7\x8b'), (2, b'\xe5\xb7\xb2\xe7\xbb\x8f\xe7\xbb\x93\xe6\x9d\x9f')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('host', models.ForeignKey(verbose_name=b'\xe4\xb8\xbb\xe5\x8a\x9e\xe6\x96\xb9', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
