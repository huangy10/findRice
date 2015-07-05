# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Activity', '0016_auto_20150704_1032'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLikeThrough',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('like_at', models.DateTimeField(auto_now_add=True)),
                ('activity', models.ForeignKey(related_name='like_through', to='Activity.Activity')),
                ('user', models.ForeignKey(related_name='like_through', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='applicationthrough',
            name='activity',
            field=models.ForeignKey(related_name='applications_through', to='Activity.Activity'),
        ),
        migrations.AddField(
            model_name='activity',
            name='liked_by',
            field=models.ManyToManyField(related_name='liked_activity', through='Activity.ActivityLikeThrough', to=settings.AUTH_USER_MODEL),
        ),
    ]
