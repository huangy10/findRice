# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Promotion', '0003_auto_20150630_1656'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sharerecord',
            old_name='create_at',
            new_name='created_at',
        ),
    ]
