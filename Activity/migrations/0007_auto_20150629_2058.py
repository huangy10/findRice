# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0006_auto_20150629_2056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='share',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='share',
            name='user',
        ),
        migrations.DeleteModel(
            name='Share',
        ),
    ]
