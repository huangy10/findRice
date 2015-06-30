# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'\xe5\xb0\x9a\xe6\x9c\xaa\xe5\xbc\x80\xe5\xa7\x8b'), (1, b'\xe5\xb7\xb2\xe7\xbb\x8f\xe5\xbc\x80\xe5\xa7\x8b'), (2, b'\xe5\xb7\xb2\xe7\xbb\x8f\xe7\xbb\x93\xe6\x9d\x9f')]),
        ),
    ]
