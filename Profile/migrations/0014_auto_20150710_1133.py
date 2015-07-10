# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0013_auto_20150708_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birthDate',
            field=models.DateField(default=b'', verbose_name=b'\xe5\x87\xba\xe7\x94\x9f\xe6\x97\xa5\xe6\x9c\x9f'),
        ),
    ]
