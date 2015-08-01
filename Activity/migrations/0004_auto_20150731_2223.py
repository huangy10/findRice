# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0003_activity_reward_share_limit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='reward_for_share',
            field=models.IntegerField(default=0),
        ),
    ]
