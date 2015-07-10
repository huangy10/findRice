# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0011_auto_20150706_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(default=b'\xe5\xa7\x93\xe5\x90\x8d', max_length=50),
        ),
    ]
