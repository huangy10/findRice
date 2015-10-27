# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0008_auto_20150831_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='reward_gift',
            field=models.BooleanField(default=False, verbose_name=b'\xe7\xa4\xbc\xe5\x93\x81'),
        ),
    ]
