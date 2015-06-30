# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Profile.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phoneNum', models.CharField(max_length=20, verbose_name=b'\xe7\x94\xb5\xe8\xaf\x9d\xe5\x8f\xb7\xe7\xa0\x81')),
                ('groupName', models.CharField(max_length=200, verbose_name=b'\xe5\x85\xac\xe5\x8f\xb8\xe5\x90\x8d\xe7\xa7\xb0')),
                ('age', models.PositiveIntegerField(verbose_name=b'\xe5\xb9\xb4\xe9\xbe\x84', editable=False)),
                ('birthDate', models.DateField(verbose_name=b'\xe5\x87\xba\xe7\x94\x9f\xe6\x97\xa5\xe6\x9c\x9f')),
                ('gender', models.SmallIntegerField(verbose_name=b'\xe6\x80\xa7\xe5\x88\xab', choices=[(0, b'\xe7\x94\xb7'), (1, b'\xe5\xa5\xb3'), (2, b'\xe4\xbf\x9d\xe5\xaf\x86')])),
                ('avatar', models.ImageField(default=b'/Users/Lena/Project/Backend/production/findRice/media/default_avatars/default_avatar.jpg', upload_to=Profile.models.get_avatar_path, verbose_name=b'\xe5\xa4\xb4\xe5\x83\x8f')),
                ('identified', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe8\xae\xa4\xe8\xaf\x81')),
                ('identified_date', models.DateField(null=True, verbose_name=b'\xe8\xae\xa4\xe8\xaf\x81\xe6\x97\xa5\xe6\x9c\x9f')),
                ('coin', models.IntegerField(verbose_name=b'\xe7\xb1\xb3\xe5\xb8\x81')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_at'],
                'verbose_name': '\u7528\u6237\u8be6\u60c5',
                'verbose_name_plural': '\u7528\u6237\u8be6\u60c5',
            },
        ),
    ]
