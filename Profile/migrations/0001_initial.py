# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import Profile.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RiceTeam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('team_coin', models.IntegerField(default=0, verbose_name=b'\xe5\x9b\xa2\xe9\x98\x9f\xe7\xb1\xb3\xe5\xb8\x81')),
                ('host', models.OneToOneField(related_name='rice_team', verbose_name=b'\xe7\xb1\xb3\xe5\x9b\xa2\xe4\xb8\xbb\xe4\xba\xba', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u7c73\u56e2',
                'verbose_name_plural': '\u7c73\u56e2',
            },
        ),
        migrations.CreateModel(
            name='RiceTeamContribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contributed_coin', models.IntegerField(default=0)),
                ('team', models.ForeignKey(to='Profile.RiceTeam')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u7c73\u56e2\u8d21\u732e',
                'verbose_name_plural': '\u7c73\u56e2\u8d21\u732e',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\xa1\xab\xe5\x86\x99\xe7\x9a\x84\xe4\xba\x86\xe8\xb4\xa6\xe6\x88\xb7\xe4\xbf\xa1\xe6\x81\xaf')),
                ('name', models.CharField(default=b'', max_length=50)),
                ('phoneNum', models.CharField(default=b'', max_length=20, verbose_name=b'\xe7\x94\xb5\xe8\xaf\x9d\xe5\x8f\xb7\xe7\xa0\x81')),
                ('groupName', models.CharField(default=b'', max_length=200, verbose_name=b'\xe5\x85\xac\xe5\x8f\xb8\xe5\x90\x8d\xe7\xa7\xb0')),
                ('birthDate', models.DateField(default=b'', verbose_name=b'\xe5\x87\xba\xe7\x94\x9f\xe6\x97\xa5\xe6\x9c\x9f')),
                ('gender', models.CharField(max_length=2, verbose_name=b'\xe6\x80\xa7\xe5\x88\xab', choices=[(b'm', b'\xe7\x94\xb7'), (b'f', b'\xe5\xa5\xb3'), (b'u', b'\xe6\x9c\xaa\xe7\x9f\xa5')])),
                ('avatar', models.ImageField(default=b'default_avatars/default_avatar.png', upload_to=Profile.models.get_avatar_path, verbose_name=b'\xe5\xa4\xb4\xe5\x83\x8f')),
                ('identified', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe8\xae\xa4\xe8\xaf\x81')),
                ('identified_date', models.DateField(verbose_name=b'\xe8\xae\xa4\xe8\xaf\x81\xe6\x97\xa5\xe6\x9c\x9f', null=True, editable=False)),
                ('coin', models.IntegerField(default=0, verbose_name=b'\xe7\xb1\xb3\xe5\xb8\x81')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('promotion_code', models.CharField(max_length=100, null=True, editable=False)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_at'],
                'verbose_name': '\u7528\u6237\u8be6\u60c5',
                'verbose_name_plural': '\u7528\u6237\u8be6\u60c5',
            },
        ),
        migrations.CreateModel(
            name='VerifyCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phoneNum', models.CharField(max_length=20, verbose_name=b'\xe5\x8f\xb7\xe7\xa0\x81')),
                ('code', models.CharField(max_length=6, verbose_name=b'\xe9\xaa\x8c\xe8\xaf\x81\xe7\xa0\x81')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'verbose_name': '\u9a8c\u8bc1\u7801',
                'verbose_name_plural': '\u9a8c\u8bc1\u7801',
            },
        ),
        migrations.AddField(
            model_name='riceteam',
            name='members',
            field=models.ManyToManyField(related_name='rice_team_as_member', verbose_name=b'\xe7\xb1\xb3\xe5\x9b\xa2\xe6\x88\x90\xe5\x91\x98', through='Profile.RiceTeamContribution', to=settings.AUTH_USER_MODEL),
        ),
    ]
