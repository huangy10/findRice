# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0008_auto_20150629_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='host_name',
            field=models.CharField(default='-', max_length=50, verbose_name=b'\xe4\xb8\xbb\xe5\x8a\x9e\xe6\x96\xb9\xe5\x90\x8d\xe7\xa7\xb0'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activity',
            name='manually_end_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 30, 8, 25, 24, 176039, tzinfo=utc), verbose_name=b'\xe6\x89\x8b\xe5\x8a\xa8\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe9\x97\xb4'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activity',
            name='manually_start_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 30, 8, 25, 30, 823648, tzinfo=utc), verbose_name=b'\xe6\x89\x8b\xe5\x8a\xa8\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='activity',
            name='applied_by',
            field=models.ManyToManyField(related_name='applied_acts', verbose_name=b'\xe7\x94\xb3\xe8\xaf\xb7\xe7\x94\xa8\xe6\x88\xb7', through='Activity.AppliedBy', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='activity',
            name='approved',
            field=models.ManyToManyField(related_name='approved_acts', verbose_name=b'\xe5\xb7\xb2\xe6\x89\xb9\xe5\x87\x86\xe7\x9a\x84\xe7\x94\xb3\xe8\xaf\xb7', through='Activity.Approved', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='activity',
            name='denied',
            field=models.ManyToManyField(related_name='denied_acts', verbose_name=b'\xe5\xb7\xb2\xe6\x8b\x92\xe7\xbb\x9d\xe7\x9a\x84\xe7\x94\xb3\xe8\xaf\xb7', through='Activity.Denied', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='activity',
            name='liked_by',
            field=models.ManyToManyField(related_name='liked_acts', verbose_name=b'\xe5\x85\xb3\xe6\xb3\xa8\xe7\x9a\x84\xe7\x94\xa8\xe6\x88\xb7', through='Activity.Like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='activity',
            name='status',
            field=models.IntegerField(default=0, verbose_name=b'\xe6\xb4\xbb\xe5\x8a\xa8\xe7\x8a\xb6\xe6\x80\x81', choices=[(0, b'\xe5\xb0\x9a\xe6\x9c\xaa\xe5\xbc\x80\xe5\xa7\x8b'), (1, b'\xe5\xb7\xb2\xe7\xbb\x8f\xe5\xbc\x80\xe5\xa7\x8b'), (2, b'\xe5\xb7\xb2\xe7\xbb\x8f\xe7\xbb\x93\xe6\x9d\x9f')]),
        ),
    ]
