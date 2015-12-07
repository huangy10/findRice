# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0007_auto_20151118_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riceteamcontribution',
            name='user',
            field=models.ForeignKey(related_name='my_contributions', to=settings.AUTH_USER_MODEL),
        ),
    ]
