# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0002_auto_20150725_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='reward_share_limit',
            field=models.IntegerField(default=500, verbose_name=b'\xe5\x88\x86\xe4\xba\xab\xe5\xa5\x96\xe5\x8a\xb1\xe4\xb8\x8a\xe9\x99\x90'),
        ),
    ]
