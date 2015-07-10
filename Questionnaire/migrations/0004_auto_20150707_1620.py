# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Questionnaire', '0003_fileanswer_is_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='choice',
            options={'ordering': ['order_in_list'], 'verbose_name': '\u9009\u9879', 'verbose_name_plural': '\u9009\u9879'},
        ),
        migrations.AlterModelOptions(
            name='questionnaire',
            options={'ordering': ['-created_at'], 'verbose_name': '\u95ee\u5377', 'verbose_name_plural': '\u95ee\u5377'},
        ),
    ]
