# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0003_auto_20150611_2251'),
    ]

    operations = [
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('activity', models.ForeignKey(to='Activity.Activity')),
            ],
            options={
                'ordering': ['-modified_at'],
                'verbose_name': '\u95ee\u5377',
                'verbose_name_plural': '\u95ee\u5377',
            },
        ),
    ]
