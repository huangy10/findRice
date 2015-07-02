# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Welfare', '0001_initial'),
        ('Activity', '0014_auto_20150702_1142'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(default=b'', max_length=255)),
                ('read', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\xb7\xb2\xe9\x98\x85')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('notification_type', models.CharField(max_length=20, verbose_name=b'\xe6\xb6\x88\xe6\x81\xaf\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(b'ready_requested', b'\xe5\xb0\xb1\xe4\xbd\x8d\xe7\xa1\xae\xe8\xae\xa4'), (b'apply_approved', b'\xe7\x94\xb3\xe8\xaf\xb7\xe9\x80\x9a\xe8\xbf\x87'), (b'apply_full', b'\xe6\x8a\xa5\xe5\x90\x8d\xe6\xbb\xa1'), (b'ready_rejected', b'\xe6\x8b\x92\xe7\xbb\x9d\xe5\xb0\xb1\xe4\xbd\x8d'), (b'share_finished', b'\xe5\x88\x86\xe4\xba\xab\xe5\xae\x8c\xe6\x88\x90')])),
            ],
            options={
                'verbose_name': '\u901a\u77e5',
                'verbose_name_plural': '\u901a\u77e5',
            },
        ),
        migrations.CreateModel(
            name='NotificationCenter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(related_name='notification_center', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SystemNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(default=b'', max_length=255)),
                ('read', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\xb7\xb2\xe9\x98\x85')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('notification_center', models.ForeignKey(related_name='system_notifications', to='Notification.NotificationCenter')),
            ],
            options={
                'verbose_name': '\u7cfb\u7edf\u6d88\u606f',
                'verbose_name_plural': '\u7cfb\u7edf\u6d88\u606f',
            },
        ),
        migrations.CreateModel(
            name='WelfareNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(default=b'', max_length=255)),
                ('read', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\xb7\xb2\xe9\x98\x85')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('gift', models.ForeignKey(to='Welfare.WelfareGift', null=True)),
                ('notification_center', models.ForeignKey(related_name='welfare_notifications', to='Notification.NotificationCenter')),
                ('related_activity', models.ForeignKey(to='Activity.Activity', null=True)),
            ],
            options={
                'verbose_name': '\u798f\u5229',
                'verbose_name_plural': '\u798f\u5229',
            },
        ),
        migrations.AddField(
            model_name='activitynotification',
            name='notification_center',
            field=models.ForeignKey(related_name='activity_notifications', to='Notification.NotificationCenter'),
        ),
        migrations.AddField(
            model_name='activitynotification',
            name='related_activity',
            field=models.ForeignKey(to='Activity.Activity'),
        ),
        migrations.AddField(
            model_name='activitynotification',
            name='related_user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
