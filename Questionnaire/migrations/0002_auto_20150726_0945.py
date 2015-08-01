# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Questionnaire', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='choicequestion',
            options={'ordering': ['created_at'], 'verbose_name': '\u9009\u62e9\u9898', 'verbose_name_plural': '\u9009\u62e9\u9898'},
        ),
        migrations.AlterModelOptions(
            name='nonchoicequestion',
            options={'ordering': ['created_at'], 'verbose_name': '\u4e3b\u89c2\u9898', 'verbose_name_plural': '\u4e3b\u89c2\u9898'},
        ),
        migrations.AddField(
            model_name='choicequestion',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 26, 1, 44, 50, 127970, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nonchoicequestion',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 26, 1, 45, 6, 606635, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
