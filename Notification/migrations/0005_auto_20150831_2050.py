# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Notification', '0004_activitynotification_reserved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitynotification',
            name='notification_type',
            field=models.CharField(max_length=20, verbose_name=b'\xe6\xb6\x88\xe6\x81\xaf\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(b'ready_requested', b'\xe5\xb0\xb1\xe4\xbd\x8d\xe7\xa1\xae\xe8\xae\xa4'), (b'apply_approved', b'\xe7\x94\xb3\xe8\xaf\xb7\xe9\x80\x9a\xe8\xbf\x87'), (b'apply_rejected', b'\xe7\x94\xb3\xe8\xaf\xb7\xe8\xa2\xab\xe6\x8b\x92'), (b'apply_full', b'\xe6\x8a\xa5\xe5\x90\x8d\xe6\xbb\xa1'), (b'ready_rejected', b'\xe6\x8b\x92\xe7\xbb\x9d\xe5\xb0\xb1\xe4\xbd\x8d'), (b'share_finished', b'\xe5\x88\x86\xe4\xba\xab\xe5\xae\x8c\xe6\x88\x90'), (b'activity_applied', b'\xe6\x9c\x89\xe4\xba\xba\xe6\x8a\xa5\xe5\x90\x8d'), (b'activity_finished', b'\xe5\xae\x8c\xe6\x88\x90\xe6\xb4\xbb\xe5\x8a\xa8'), (b'activity_deleted', b'\xe6\xb4\xbb\xe5\x8a\xa8\xe5\x88\xa0\xe9\x99\xa4')]),
        ),
    ]
