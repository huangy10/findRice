# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0020_auto_20150706_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_type',
            field=models.ForeignKey(to='Activity.ActivityType', null=True),
        ),
    ]
