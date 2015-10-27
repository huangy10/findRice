# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Profile.models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0002_auto_20150803_2258'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar_zipped',
            field=models.ImageField(upload_to=Profile.models.get_avatar_path_zipped, null=True, editable=False, blank=True),
        ),
    ]
