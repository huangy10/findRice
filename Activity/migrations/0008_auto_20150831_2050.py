# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Activity.models


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0007_auto_20150812_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='poster',
            field=models.ImageField(upload_to=Activity.models.get_activity_poster_path, null=True, verbose_name=b'\xe6\xb5\xb7\xe6\x8a\xa5', blank=True),
        ),
    ]
