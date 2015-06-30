# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Activity', '0005_auto_20150629_1459'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type_name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=100)),
                ('display_order', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '\u6d3b\u52a8\u7c7b\u578b',
                'verbose_name_plural': '\u6d3b\u52a8\u7c7b\u578b',
            },
        ),
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reward', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': '\u5206\u4eab',
                'verbose_name_plural': '\u5206\u4eab',
            },
        ),
        migrations.AddField(
            model_name='activity',
            name='recommended_level',
            field=models.IntegerField(default=0, verbose_name=b'\xe6\x8e\xa8\xe8\x8d\x90\xe7\xad\x89\xe7\xba\xa7'),
        ),
        migrations.AddField(
            model_name='share',
            name='activity',
            field=models.ForeignKey(to='Activity.Activity'),
        ),
        migrations.AddField(
            model_name='share',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activity',
            name='activity_type',
            field=models.ManyToManyField(to='Activity.ActivityType'),
        ),
    ]
