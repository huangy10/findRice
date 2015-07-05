# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Profile.models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0007_auto_20150704_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default=b'media/default_avatars/default_avatar.jpg', upload_to=Profile.models.get_avatar_path, verbose_name=b'\xe5\xa4\xb4\xe5\x83\x8f'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(default=b'u', max_length=2, verbose_name=b'\xe6\x80\xa7\xe5\x88\xab', choices=[(b'm', b'\xe7\x94\xb7'), (b'f', b'\xe5\xa5\xb3'), (b'u', b'\xe6\x9c\xaa\xe7\x9f\xa5')]),
        ),
    ]
