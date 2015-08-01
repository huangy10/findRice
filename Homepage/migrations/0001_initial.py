# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Homepage.models


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomepageIssue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('issue_num', models.IntegerField(default=1)),
            ],
            options={
                'ordering': ['-created_at'],
                'verbose_name': '\u9996\u9875',
                'verbose_name_plural': '\u9996\u9875',
            },
        ),
        migrations.CreateModel(
            name='HomepagePoster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('poster', models.ImageField(upload_to=Homepage.models.get_poster_path, verbose_name=b'\xe6\xb5\xb7\xe6\x8a\xa5')),
                ('poster_type', models.IntegerField(choices=[(0, b'banner'), (1, b'footer')])),
                ('issue', models.ForeignKey(to='Homepage.HomepageIssue')),
                ('related_activity', models.ForeignKey(verbose_name=b'\xe7\x9b\xb8\xe5\x85\xb3\xe6\xb4\xbb\xe5\x8a\xa8', to='Activity.Activity')),
            ],
            options={
                'verbose_name': '\u9996\u9875',
                'verbose_name_plural': '\u9996\u9875',
            },
        ),
    ]
