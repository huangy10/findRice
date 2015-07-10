# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import findRice.utils
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Promotion', '0007_auto_20150701_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='share',
            name='activity',
            field=models.ForeignKey(to='Activity.Activity', validators=[findRice.utils.field_is_active_validator]),
        ),
        migrations.AlterField(
            model_name='share',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, validators=[findRice.utils.field_is_active_validator]),
        ),
        migrations.AlterField(
            model_name='sharerecord',
            name='application',
            field=models.OneToOneField(related_name='share_record', null=True, default=None, validators=[findRice.utils.field_is_active_validator], to='Activity.ApplicationThrough'),
        ),
        migrations.AlterField(
            model_name='sharerecord',
            name='share',
            field=models.ForeignKey(to='Promotion.Share', validators=[findRice.utils.field_is_active_validator]),
        ),
        migrations.AlterField(
            model_name='sharerecord',
            name='target_user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, validators=[findRice.utils.field_is_active_validator]),
        ),
    ]
