# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Activity', '0010_auto_20150630_1643'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationThrough',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('apply_at', models.DateTimeField(verbose_name=b'\xe7\x94\xb3\xe8\xaf\xb7\xe6\x97\xa5\xe6\x9c\x9f')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.SmallIntegerField(default=0, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[(0, b'\xe7\x94\xb3\xe8\xaf\xb7\xe4\xb8\xad'), (1, b'\xe5\xb7\xb2\xe6\x89\xb9\xe5\x87\x86'), (2, b'\xe5\xb7\xb2\xe6\x8b\x92\xe7\xbb\x9d'), (3, b'\xe5\xb7\xb2\xe5\xae\x8c\xe6\x88\x90')])),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': '\u53c2\u4e0e',
                'verbose_name_plural': '\u53c2\u4e0e',
            },
        ),
        migrations.AlterUniqueTogether(
            name='appliedby',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='appliedby',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='appliedby',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='approved',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='approved',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='approved',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='denied',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='denied',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='denied',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='like',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='like',
            name='user',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='applied_by',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='approved',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='denied',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='liked_by',
        ),
        migrations.DeleteModel(
            name='AppliedBy',
        ),
        migrations.DeleteModel(
            name='Approved',
        ),
        migrations.DeleteModel(
            name='Denied',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
        migrations.AddField(
            model_name='applicationthrough',
            name='activity',
            field=models.ForeignKey(related_name='application_through', to='Activity.Activity'),
        ),
        migrations.AddField(
            model_name='applicationthrough',
            name='user',
            field=models.ForeignKey(related_name='applications_through', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activity',
            name='candidates',
            field=models.ManyToManyField(related_name='applied_activity', through='Activity.ApplicationThrough', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='applicationthrough',
            unique_together=set([('activity', 'user')]),
        ),
    ]
