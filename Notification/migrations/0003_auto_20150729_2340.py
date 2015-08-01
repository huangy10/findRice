# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Notification', '0002_auto_20150727_1337'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activitynotification',
            options={'ordering': ['-created_at'], 'verbose_name': '\u901a\u77e5', 'verbose_name_plural': '\u901a\u77e5'},
        ),
        migrations.AlterModelOptions(
            name='systemnotification',
            options={'ordering': ['-created_at'], 'verbose_name': '\u7cfb\u7edf\u6d88\u606f', 'verbose_name_plural': '\u7cfb\u7edf\u6d88\u606f'},
        ),
        migrations.AlterModelOptions(
            name='welfarenotification',
            options={'ordering': ['-created_at'], 'verbose_name': '\u798f\u5229', 'verbose_name_plural': '\u798f\u5229'},
        ),
    ]
