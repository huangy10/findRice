# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Notification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='welfarenotification',
            name='related_activity',
            field=models.ForeignKey(to='Activity.Activity'),
        ),
    ]
