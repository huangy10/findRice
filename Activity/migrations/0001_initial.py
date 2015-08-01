# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Activity.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_published', models.BooleanField(default=False)),
                ('accept_apply', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=200, verbose_name=b'\xe6\xb4\xbb\xe5\x8a\xa8\xe5\x90\x8d\xe7\xa7\xb0')),
                ('host_name', models.CharField(max_length=50, verbose_name=b'\xe4\xb8\xbb\xe5\x8a\x9e\xe6\x96\xb9\xe5\x90\x8d\xe7\xa7\xb0')),
                ('location', models.CharField(max_length=200, verbose_name=b'\xe6\xb4\xbb\xe5\x8a\xa8\xe5\x9c\xb0\xe7\x82\xb9')),
                ('province', models.CharField(max_length=20, verbose_name=b'\xe7\x9c\x81\xe4\xbb\xbd')),
                ('city', models.CharField(max_length=100, verbose_name=b'\xe5\x9f\x8e\xe5\xb8\x82')),
                ('description', models.TextField(verbose_name=b'\xe6\xb4\xbb\xe5\x8a\xa8\xe7\xae\x80\xe4\xbb\x8b')),
                ('start_time', models.DateTimeField(verbose_name=b'\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4')),
                ('end_time', models.DateTimeField(verbose_name=b'\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe9\x97\xb4')),
                ('last_length', models.IntegerField(verbose_name=b'\xe6\x8c\x81\xe7\xbb\xad\xe6\x97\xb6\xe9\x97\xb4(min)')),
                ('reward', models.IntegerField(verbose_name=b'\xe5\xa5\x96\xe5\x8a\xb1\xe9\x87\x91\xe9\xa2\x9d')),
                ('reward_for_share', models.IntegerField(default=5)),
                ('reward_for_share_and_finished_percentage', models.FloatField(default=0.1)),
                ('max_attend', models.IntegerField(default=10, verbose_name=b'\xe5\x85\x81\xe8\xae\xb8\xe6\x8a\xa5\xe5\x90\x8d\xe7\x9a\x84\xe6\x9c\x80\xe5\xa4\xa7\xe4\xba\xba\xe6\x95\xb0')),
                ('min_attend', models.IntegerField(default=0, verbose_name=b'\xe6\x9c\x80\xe5\xb0\x91\xe9\x9c\x80\xe8\xa6\x81\xe7\x9a\x84\xe4\xba\xba\xe6\x95\xb0')),
                ('poster', models.ImageField(default=b'defaultPosters/default.jpg', upload_to=Activity.models.get_activity_poster_path, verbose_name=b'\xe6\xb5\xb7\xe6\x8a\xa5')),
                ('recommended', models.BooleanField(default=False, verbose_name=b'\xe7\x83\xad\xe9\x97\xa8\xe6\x8e\xa8\xe8\x8d\x90')),
                ('recommended_level', models.IntegerField(default=0, verbose_name=b'\xe6\x8e\xa8\xe8\x8d\x90\xe7\xad\x89\xe7\xba\xa7')),
                ('time_limited', models.BooleanField(default=False, verbose_name=b'\xe9\x99\x90\xe6\x97\xb6\xe6\x8a\xa5\xe5\x90\x8d')),
                ('num_limited', models.BooleanField(default=False, verbose_name=b'\xe9\x99\x90\xe9\xa2\x9d\xe6\x8a\xa5\xe5\x90\x8d')),
                ('identified', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe8\xae\xa4\xe8\xaf\x81')),
                ('act_status', models.IntegerField(default=0, verbose_name=b'\xe6\xb4\xbb\xe5\x8a\xa8\xe7\x8a\xb6\xe6\x80\x81', choices=[(0, b'\xe5\xb0\x9a\xe6\x9c\xaa\xe5\xbc\x80\xe5\xa7\x8b'), (1, b'\xe5\xb7\xb2\xe7\xbb\x8f\xe5\xbc\x80\xe5\xa7\x8b'), (2, b'\xe5\xb7\xb2\xe7\xbb\x8f\xe7\xbb\x93\xe6\x9d\x9f')])),
                ('manually_start_time', models.DateTimeField(verbose_name=b'\xe6\x89\x8b\xe5\x8a\xa8\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4', null=True, editable=False)),
                ('manually_end_time', models.DateTimeField(verbose_name=b'\xe6\x89\x8b\xe5\x8a\xa8\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe9\x97\xb4', null=True, editable=False)),
                ('viewed_times', models.BigIntegerField(default=0, verbose_name=b'\xe6\xb5\x8f\xe8\xa7\x88\xe6\xac\xa1\xe6\x95\xb0')),
            ],
            options={
                'ordering': ['-created_at'],
                'verbose_name': '\u6d3b\u52a8',
                'verbose_name_plural': '\u6d3b\u52a8',
            },
        ),
        migrations.CreateModel(
            name='ActivityLikeThrough',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('like_at', models.DateTimeField(auto_now_add=True)),
                ('activity', models.ForeignKey(related_name='like_through', to='Activity.Activity')),
                ('user', models.ForeignKey(related_name='like_through', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ActivityType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type_name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=100)),
                ('display_order', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['display_order'],
                'verbose_name': '\u6d3b\u52a8\u7c7b\u578b',
                'verbose_name_plural': '\u6d3b\u52a8\u7c7b\u578b',
            },
        ),
        migrations.CreateModel(
            name='ActivityVisitRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('visit_date', models.DateTimeField(auto_now_add=True)),
                ('visit_ip', models.GenericIPAddressField(default=b'0.0.0.0')),
                ('visit_location', models.CharField(default=b'-', max_length=255)),
                ('visit_device', models.CharField(default=b'-', max_length=255)),
                ('activity', models.ForeignKey(to='Activity.Activity')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u8bbf\u95ee\u8bb0\u5f55',
                'verbose_name_plural': '\u8bbf\u95ee\u8bb0\u5f55',
            },
        ),
        migrations.CreateModel(
            name='ApplicationThrough',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('apply_at', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe7\x94\xb3\xe8\xaf\xb7\xe6\x97\xa5\xe6\x9c\x9f')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default=b'applying', max_length=10, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[(b'applying', b'\xe7\x94\xb3\xe8\xaf\xb7\xe4\xb8\xad'), (b'approved', b'\xe5\xb7\xb2\xe6\x89\xb9\xe5\x87\x86'), (b'ready', b'\xe5\xb7\xb2\xe5\xb0\xb1\xe4\xbd\x8d'), (b'denied', b'\xe5\xb7\xb2\xe6\x8b\x92\xe7\xbb\x9d'), (b'finished', b'\xe5\xb7\xb2\xe5\xae\x8c\xe6\x88\x90')])),
                ('is_active', models.BooleanField(default=True, help_text=b"don't set this manually")),
                ('activity', models.ForeignKey(related_name='applications_through', to='Activity.Activity')),
                ('user', models.ForeignKey(related_name='applications_through', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-apply_at'],
                'verbose_name': '\u53c2\u4e0e',
                'verbose_name_plural': '\u53c2\u4e0e',
            },
        ),
        migrations.AddField(
            model_name='activity',
            name='activity_type',
            field=models.ForeignKey(to='Activity.ActivityType', null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='backup',
            field=models.ForeignKey(related_name='master', blank=True, to='Activity.Activity', null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='candidates',
            field=models.ManyToManyField(related_name='applied_activity', through='Activity.ApplicationThrough', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activity',
            name='host',
            field=models.ForeignKey(verbose_name=b'\xe4\xb8\xbb\xe5\x8a\x9e\xe6\x96\xb9', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activity',
            name='liked_by',
            field=models.ManyToManyField(related_name='liked_activity', through='Activity.ActivityLikeThrough', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='applicationthrough',
            unique_together=set([('activity', 'user')]),
        ),
    ]
