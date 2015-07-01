# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0009_auto_20150630_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='manually_end_time',
            field=models.DateTimeField(null=True, verbose_name=b'\xe6\x89\x8b\xe5\x8a\xa8\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='manually_start_time',
            field=models.DateTimeField(null=True, verbose_name=b'\xe6\x89\x8b\xe5\x8a\xa8\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4'),
        ),
    ]
