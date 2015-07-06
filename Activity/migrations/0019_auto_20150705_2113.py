# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0018_auto_20150705_0730'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activitytype',
            options={'ordering': ['-created_at'], 'verbose_name': '\u6d3b\u52a8\u7c7b\u578b', 'verbose_name_plural': '\u6d3b\u52a8\u7c7b\u578b'},
        ),
    ]
