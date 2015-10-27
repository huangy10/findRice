# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Activity.models


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0010_activity_reward_gift_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='poster_thumbnail',
            field=models.ImageField(upload_to=Activity.models.get_activity_poster_path_zipped, null=True, verbose_name=b'\xe6\xb5\xb7\xe6\x8a\xa5\xe7\xbc\xa9\xe7\x95\xa5\xe5\x9b\xbe', blank=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='reward_for_share',
            field=models.IntegerField(default=0),
        ),
    ]
