# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0012_auto_20150701_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationthrough',
            name='is_active',
            field=models.BooleanField(default=True, help_text=b"don't set this manually"),
        ),
    ]
