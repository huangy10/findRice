# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Promotion', '0006_sharerecord_application'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharerecord',
            name='application',
            field=models.OneToOneField(related_name='share_record', null=True, default=None, to='Activity.ApplicationThrough'),
        ),
    ]
