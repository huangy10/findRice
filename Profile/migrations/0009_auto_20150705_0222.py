# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0008_auto_20150705_0150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riceteam',
            name='members',
            field=models.ManyToManyField(related_name='rice_team_as_member', verbose_name=b'\xe7\xb1\xb3\xe5\x9b\xa2\xe6\x88\x90\xe5\x91\x98', through='Profile.RiceTeamContribution', to=settings.AUTH_USER_MODEL),
        ),
    ]
