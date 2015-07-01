# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Promotion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='share',
            name='share_line',
            field=models.CharField(default='', max_length=100, editable=False),
            preserve_default=False,
        ),
    ]
