# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0010_auto_20150630_1643'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_reward_max', models.IntegerField(default=500)),
                ('total_reward', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('activity', models.ForeignKey(to='Activity.Activity')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u5206\u4eab',
                'verbose_name_plural': '\u5206\u4eab',
            },
        ),
        migrations.CreateModel(
            name='ShareRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x86\xe4\xba\xab\xe6\x97\xa5\xe6\x9c\x9f')),
                ('finished', models.BooleanField(default=False)),
                ('share', models.ForeignKey(to='Promotion.Share')),
                ('target_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u5206\u4eab',
                'verbose_name_plural': '\u5206\u4eab',
            },
        ),
        migrations.AlterUniqueTogether(
            name='sharerecord',
            unique_together=set([('share', 'target_user')]),
        ),
        migrations.AlterUniqueTogether(
            name='share',
            unique_together=set([('user', 'activity')]),
        ),
    ]
