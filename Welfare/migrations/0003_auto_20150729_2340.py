# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Welfare', '0002_auto_20150727_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='welfaregift',
            name='getted_date',
            field=models.DateTimeField(null=True, verbose_name=b'\xe5\x8f\x96\xe7\x8e\xb0\xe6\x97\xa5\xe6\x9c\x9f', blank=True),
        ),
        migrations.AlterField(
            model_name='welfaregift',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'\xe7\x94\xb3\xe8\xaf\xb7\xe5\x85\x91\xe6\x8d\xa2\xe7\x9a\x84\xe6\x97\xa5\xe6\x9c\x9f'),
        ),
        migrations.AlterField(
            model_name='welfaregift',
            name='target',
            field=models.ForeignKey(verbose_name=b'\xe7\x9b\xae\xe6\xa0\x87\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL),
        ),
    ]
