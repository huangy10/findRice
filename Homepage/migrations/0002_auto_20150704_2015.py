# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='homepageissue',
            options={'ordering': ['-created_at'], 'verbose_name': '\u9996\u9875', 'verbose_name_plural': '\u9996\u9875'},
        ),
    ]
