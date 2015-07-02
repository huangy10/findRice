# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0013_auto_20150701_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationthrough',
            name='status',
            field=models.CharField(default=b'applying', max_length=10, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[(b'applying', b'\xe7\x94\xb3\xe8\xaf\xb7\xe4\xb8\xad'), (b'approved', b'\xe5\xb7\xb2\xe6\x89\xb9\xe5\x87\x86'), (b'denied', b'\xe5\xb7\xb2\xe6\x8b\x92\xe7\xbb\x9d'), (b'finished', b'\xe5\xb7\xb2\xe5\xae\x8c\xe6\x88\x90')]),
        ),
    ]
