# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Promotion', '0002_share_share_line'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='share',
            name='share_line',
        ),
        migrations.AddField(
            model_name='share',
            name='share_code',
            field=models.CharField(max_length=100, null=True, editable=False),
        ),
    ]
