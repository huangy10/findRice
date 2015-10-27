# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Profile.models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0004_auto_20150812_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='riceteamcontribution',
            name='registration_promoted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(upload_to=Profile.models.get_avatar_path, null=True, verbose_name=b'\xe5\xa4\xb4\xe5\x83\x8f', blank=True),
        ),
    ]
