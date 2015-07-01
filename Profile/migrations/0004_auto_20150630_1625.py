# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Profile', '0003_auto_20150627_2325'),
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
        migrations.AddField(
            model_name='userprofile',
            name='name',
            field=models.CharField(default=b'-', max_length=50),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='identified_date',
            field=models.DateField(verbose_name=b'\xe8\xae\xa4\xe8\xaf\x81\xe6\x97\xa5\xe6\x9c\x9f', null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='riceteam',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name=b'\xe7\xb1\xb3\xe5\x9b\xa2\xe6\x88\x90\xe5\x91\x98', through='Profile.RiceTeamContribution'),
        ),
    ]
