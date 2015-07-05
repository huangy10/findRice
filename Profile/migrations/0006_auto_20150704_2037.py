# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0005_userprofile_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.SmallIntegerField(default=2, verbose_name=b'\xe6\x80\xa7\xe5\x88\xab', choices=[(b'm', b'\xe7\x94\xb7'), (b'f', b'\xe5\xa5\xb3'), (b'u', b'\xe4\xbf\x9d\xe5\xaf\x86')]),
        ),
    ]
