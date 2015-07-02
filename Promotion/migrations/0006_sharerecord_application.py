# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0012_auto_20150701_1915'),
        ('Promotion', '0005_auto_20150630_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='sharerecord',
            name='application',
            field=models.OneToOneField(related_name='share_record', default=None, to='Activity.ApplicationThrough'),
            preserve_default=False,
        ),
    ]
