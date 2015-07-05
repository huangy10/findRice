# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Activity', '0014_auto_20150702_1142'),
    ]

    operations = [
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
    ]
