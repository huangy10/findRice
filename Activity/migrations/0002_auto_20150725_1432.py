# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitytype',
            name='display_order',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
