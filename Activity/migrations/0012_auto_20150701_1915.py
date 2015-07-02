# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0011_auto_20150701_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationthrough',
            name='apply_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'\xe7\x94\xb3\xe8\xaf\xb7\xe6\x97\xa5\xe6\x9c\x9f'),
        ),
    ]
