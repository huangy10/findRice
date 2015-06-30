# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Activity', '0003_auto_20150611_2251'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppliedBy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('apply_date', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': '\u7533\u8bf7',
                'verbose_name_plural': '\u7533\u8bf7',
            },
        ),
        migrations.CreateModel(
            name='Approved',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('approve_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': '\u6279\u51c6',
                'verbose_name_plural': '\u6279\u51c6',
            },
        ),
        migrations.CreateModel(
            name='Denied',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deny_date', models.DateTimeField(auto_now=True)),
                ('deny_reason', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': '\u62d2\u7edd',
                'verbose_name_plural': '\u62d2\u7edd',
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('like_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': '\u559c\u6b22',
                'verbose_name_plural': '\u559c\u6b22',
            },
        ),
        migrations.AddField(
            model_name='activity',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='like',
            name='activity',
            field=models.ForeignKey(related_name='like_relation', to='Activity.Activity'),
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(related_name='like_relation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='denied',
            name='activity',
            field=models.ForeignKey(related_name='denied_relation', to='Activity.Activity'),
        ),
        migrations.AddField(
            model_name='denied',
            name='user',
            field=models.ForeignKey(related_name='denied_relation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='approved',
            name='activity',
            field=models.ForeignKey(related_name='approved_relation', to='Activity.Activity'),
        ),
        migrations.AddField(
            model_name='approved',
            name='user',
            field=models.ForeignKey(related_name='approved_relation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appliedby',
            name='activity',
            field=models.ForeignKey(related_name='applied_by_relation', to='Activity.Activity'),
        ),
        migrations.AddField(
            model_name='appliedby',
            name='user',
            field=models.ForeignKey(related_name='applied_by_relation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activity',
            name='applied_by',
            field=models.ManyToManyField(related_name='applied_acts', through='Activity.AppliedBy', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activity',
            name='approved',
            field=models.ManyToManyField(related_name='approved_acts', through='Activity.Approved', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activity',
            name='denied',
            field=models.ManyToManyField(related_name='denied_acts', through='Activity.Denied', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activity',
            name='liked_by',
            field=models.ManyToManyField(related_name='liked_acts', through='Activity.Like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='denied',
            unique_together=set([('activity', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='approved',
            unique_together=set([('activity', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='appliedby',
            unique_together=set([('activity', 'user')]),
        ),
    ]
