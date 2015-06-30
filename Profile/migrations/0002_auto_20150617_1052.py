# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='age',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='birthDate',
            field=models.DateField(default=datetime.datetime(1970, 1, 1, 0, 0), verbose_name=b'\xe5\x87\xba\xe7\x94\x9f\xe6\x97\xa5\xe6\x9c\x9f'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='coin',
            field=models.IntegerField(default=0, verbose_name=b'\xe7\xb1\xb3\xe5\xb8\x81'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.SmallIntegerField(default=2, verbose_name=b'\xe6\x80\xa7\xe5\x88\xab', choices=[(0, b'\xe7\x94\xb7'), (1, b'\xe5\xa5\xb3'), (2, b'\xe4\xbf\x9d\xe5\xaf\x86')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='groupName',
            field=models.CharField(default=b'-', max_length=200, verbose_name=b'\xe5\x85\xac\xe5\x8f\xb8\xe5\x90\x8d\xe7\xa7\xb0'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phoneNum',
            field=models.CharField(default=b'-', max_length=20, verbose_name=b'\xe7\x94\xb5\xe8\xaf\x9d\xe5\x8f\xb7\xe7\xa0\x81'),
        ),
    ]
