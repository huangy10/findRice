# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Questionnaire', '0002_auto_20150701_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileanswer',
            name='is_image',
            field=models.BooleanField(default=True),
        ),
    ]
