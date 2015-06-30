# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Activity.models


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0002_auto_20150611_2113'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'ordering': ['-created_at'], 'verbose_name': '\u6d3b\u52a8', 'verbose_name_plural': '\u6d3b\u52a8'},
        ),
        migrations.AlterField(
            model_name='activity',
            name='poster',
            field=models.ImageField(default=b'/Users/Lena/Project/Backend/production/findRice/media/defaultPosters/default.jpg', upload_to=Activity.models.get_activity_poster_path, verbose_name=b'\xe6\xb5\xb7\xe6\x8a\xa5'),
        ),
    ]
