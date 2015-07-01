# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Promotion', '0004_auto_20150630_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='share',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='sharerecord',
            name='actual_reward_for_finish',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sharerecord',
            name='actual_reward_for_share',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sharerecord',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
