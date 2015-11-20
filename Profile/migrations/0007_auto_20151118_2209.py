# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0006_auto_20151118_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='team_leader',
            field=models.ForeignKey(related_name='+', verbose_name=b'\xe7\xb1\xb3\xe5\x9b\xa2\xe9\x95\xbf', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
