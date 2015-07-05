# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0004_auto_20150630_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\xa1\xab\xe5\x86\x99\xe7\x9a\x84\xe4\xba\x86\xe8\xb4\xa6\xe6\x88\xb7\xe4\xbf\xa1\xe6\x81\xaf'),
        ),
    ]
