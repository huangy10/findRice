# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Activity.models


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0004_auto_20150731_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='poster_zipped',
            field=models.ImageField(upload_to=Activity.models.get_activity_poster_path, null=True, verbose_name=b'\xe5\x8e\x8b\xe7\xbc\xa9\xe6\xb5\xb7\xe6\x8a\xa5', blank=True),
        ),
    ]
