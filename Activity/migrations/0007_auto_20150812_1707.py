# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0006_auto_20150808_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='reward_for_share',
            field=models.IntegerField(default=5),
        ),
    ]
