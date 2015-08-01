# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import findRice.utils
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Activity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_reward_max', models.IntegerField(default=500)),
                ('total_reward', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('share_code', models.CharField(max_length=100, null=True, editable=False)),
                ('activity', models.ForeignKey(to='Activity.Activity', validators=[findRice.utils.field_is_active_validator])),
                ('user', models.ForeignKey(validators=[findRice.utils.field_is_active_validator], to=settings.AUTH_USER_MODEL, blank=True, null=True)),
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
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x86\xe4\xba\xab\xe6\x97\xa5\xe6\x9c\x9f')),
                ('finished', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('actual_reward_for_share', models.IntegerField(default=0)),
                ('actual_reward_for_finish', models.IntegerField(default=0)),
                ('application', models.OneToOneField(related_name='share_record', null=True, default=None, validators=[findRice.utils.field_is_active_validator], to='Activity.ApplicationThrough')),
                ('share', models.ForeignKey(to='Promotion.Share', validators=[findRice.utils.field_is_active_validator])),
                ('target_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, validators=[findRice.utils.field_is_active_validator])),
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
