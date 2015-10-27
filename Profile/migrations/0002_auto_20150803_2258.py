# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar_social',
            field=models.CharField(max_length=100, null=True, verbose_name=b'\xe7\xa4\xbe\xe4\xba\xa4\xe5\xb9\xb3\xe5\x8f\xb0\xe5\xa4\xb4\xe5\x83\x8fURL', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(default=b'\xe7\x94\xa8\xe6\x88\xb7\xe6\x98\xb5\xe7\xa7\xb0', max_length=50),
        ),
    ]
