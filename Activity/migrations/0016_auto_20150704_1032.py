# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0015_activityvisitrecord'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='activity_type',
        ),
        migrations.AddField(
            model_name='activity',
            name='activity_type',
            field=models.ForeignKey(default=None, to='Activity.ActivityType'),
            preserve_default=False,
        ),
    ]
