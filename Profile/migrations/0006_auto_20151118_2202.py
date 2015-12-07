# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Activity', '0012_activitytype_default_poster_mobile'),
        ('Profile', '0005_auto_20150831_2050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='riceteam',
            name='host',
        ),
        migrations.RemoveField(
            model_name='riceteam',
            name='members',
        ),
        migrations.RemoveField(
            model_name='riceteamcontribution',
            name='registration_promoted',
        ),
        migrations.RemoveField(
            model_name='riceteamcontribution',
            name='team',
        ),
        migrations.AddField(
            model_name='riceteamcontribution',
            name='activity',
            field=models.ForeignKey(default=0, verbose_name=b'\xe7\x9b\xb8\xe5\x85\xb3\xe6\xb4\xbb\xe5\x8a\xa8', to='Activity.Activity'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='riceteamcontribution',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 18, 14, 1, 49, 301955, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='riceteamcontribution',
            name='leader',
            field=models.ForeignKey(related_name='+', verbose_name=b'\xe7\xb1\xb3\xe5\x9b\xa2\xe9\x95\xbf', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='team_leader',
            field=models.ForeignKey(related_name='+', default=1, verbose_name=b'\xe7\xb1\xb3\xe5\x9b\xa2\xe9\x95\xbf', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='riceteamcontribution',
            name='contributed_coin',
            field=models.IntegerField(default=0, verbose_name=b'\xe8\xb4\xa1\xe7\x8c\xae\xe7\x9a\x84\xe7\xb1\xb3\xe5\xb8\x81'),
        ),
        migrations.AlterField(
            model_name='riceteamcontribution',
            name='user',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='RiceTeam',
        ),
    ]
