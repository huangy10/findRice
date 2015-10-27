# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Activity.models


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0005_activity_poster_zipped'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitytype',
            name='default_poster',
            field=models.ImageField(default=b'defaultPosters/default.jpg', upload_to=Activity.models.get_activity_poster_path, verbose_name=b'\xe9\xbb\x98\xe8\xae\xa4\xe6\xb5\xb7\xe6\x8a\xa5'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='activity_type',
            field=models.ForeignKey(default=None, verbose_name=b'\xe6\xb4\xbb\xe5\x8a\xa8\xe7\xb1\xbb\xe5\x9e\x8b', to='Activity.ActivityType'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='activity',
            name='poster',
            field=models.ImageField(upload_to=Activity.models.get_activity_poster_path, verbose_name=b'\xe6\xb5\xb7\xe6\x8a\xa5'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='poster_zipped',
            field=models.ImageField(upload_to=Activity.models.get_activity_poster_path_zipped, null=True, verbose_name=b'\xe5\x8e\x8b\xe7\xbc\xa9\xe6\xb5\xb7\xe6\x8a\xa5', blank=True),
        ),
    ]
