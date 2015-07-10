# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Profile.models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0010_verifycode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default=b'default_avatars/default_avatar.jpg', upload_to=Profile.models.get_avatar_path, verbose_name=b'\xe5\xa4\xb4\xe5\x83\x8f'),
        ),
    ]
