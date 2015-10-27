# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Activity.models


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0011_auto_20150916_2142'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitytype',
            name='default_poster_mobile',
            field=models.ImageField(default=b'defaultPosters/default.jpg', upload_to=Activity.models.get_activity_poster_path, verbose_name=b'\xe9\xbb\x98\xe8\xae\xa4\xe6\xb5\xb7\xe6\x8a\xa5(mobile)'),
        ),
    ]
