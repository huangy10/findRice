# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0009_activity_reward_gift'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='reward_gift_detail',
            field=models.TextField(default=b'', verbose_name=b'\xe7\xa4\xbc\xe5\x93\x81\xe8\xaf\xa6\xe6\x83\x85'),
        ),
    ]
