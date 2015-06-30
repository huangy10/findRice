# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0007_auto_20150629_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='min_attend',
            field=models.IntegerField(default=0, verbose_name=b'\xe6\x9c\x80\xe5\xb0\x91\xe9\x9c\x80\xe8\xa6\x81\xe7\x9a\x84\xe4\xba\xba\xe6\x95\xb0'),
        ),
        migrations.AddField(
            model_name='activity',
            name='reward_for_share',
            field=models.IntegerField(default=5),
        ),
        migrations.AddField(
            model_name='activity',
            name='reward_for_share_and_finished_percentage',
            field=models.FloatField(default=0.1),
        ),
        migrations.AlterField(
            model_name='activity',
            name='max_attend',
            field=models.IntegerField(default=10, verbose_name=b'\xe5\x85\x81\xe8\xae\xb8\xe6\x8a\xa5\xe5\x90\x8d\xe7\x9a\x84\xe6\x9c\x80\xe5\xa4\xa7\xe4\xba\xba\xe6\x95\xb0'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='reward',
            field=models.IntegerField(verbose_name=b'\xe5\xa5\x96\xe5\x8a\xb1\xe9\x87\x91\xe9\xa2\x9d'),
        ),
    ]
