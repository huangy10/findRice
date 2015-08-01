# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Welfare', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='welfaregift',
            options={'ordering': ['-created_at'], 'verbose_name': '\u798f\u5229', 'verbose_name_plural': '\u798f\u5229'},
        ),
        migrations.AddField(
            model_name='welfaregift',
            name='coin_cost',
            field=models.IntegerField(default=0, verbose_name=b'\xe6\x89\xa3\xe9\x99\xa4\xe7\xb1\xb3\xe5\xb8\x81'),
        ),
        migrations.AddField(
            model_name='welfaregift',
            name='created_at',
            field=models.DateTimeField(default=None, auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='welfaregift',
            name='getted',
            field=models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\xb7\xb2\xe7\xbb\x8f\xe8\xa2\xab\xe9\xa2\x86\xe5\x8f\x96\xe6\x88\x96\xe8\x80\x85\xe5\x85\x91\xe7\x8e\xb0'),
        ),
        migrations.AddField(
            model_name='welfaregift',
            name='rmb',
            field=models.IntegerField(default=0, verbose_name=b'\xe5\x85\x91\xe7\x8e\xb0\xe7\x9a\x84\xe7\x8e\xb0\xe9\x87\x91'),
        ),
        migrations.AddField(
            model_name='welfaregift',
            name='target',
            field=models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='welfaregift',
            name='zfb_account',
            field=models.CharField(default=b'', max_length=50, verbose_name=b'\xe6\x94\xaf\xe4\xbb\x98\xe5\xae\x9d\xe8\xb4\xa6\xe5\x8f\xb7'),
        ),
        migrations.AlterField(
            model_name='welfaregift',
            name='address',
            field=models.CharField(max_length=255, null=True, verbose_name=b'\xe5\x9c\xb0\xe5\x9d\x80', blank=True),
        ),
    ]
