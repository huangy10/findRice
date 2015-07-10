# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0019_auto_20150705_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='viewed_times',
            field=models.BigIntegerField(default=0, verbose_name=b'\xe6\xb5\x8f\xe8\xa7\x88\xe6\xac\xa1\xe6\x95\xb0'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='manually_end_time',
            field=models.DateTimeField(verbose_name=b'\xe6\x89\x8b\xe5\x8a\xa8\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe9\x97\xb4', null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='activity',
            name='manually_start_time',
            field=models.DateTimeField(verbose_name=b'\xe6\x89\x8b\xe5\x8a\xa8\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4', null=True, editable=False),
        ),
    ]
