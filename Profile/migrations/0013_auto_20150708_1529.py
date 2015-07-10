# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0012_auto_20150708_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='groupName',
            field=models.CharField(default=b'', max_length=200, verbose_name=b'\xe5\x85\xac\xe5\x8f\xb8\xe5\x90\x8d\xe7\xa7\xb0'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phoneNum',
            field=models.CharField(default=b'', max_length=20, verbose_name=b'\xe7\x94\xb5\xe8\xaf\x9d\xe5\x8f\xb7\xe7\xa0\x81'),
        ),
    ]
