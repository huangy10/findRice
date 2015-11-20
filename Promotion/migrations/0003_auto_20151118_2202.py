# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Activity', '0012_activitytype_default_poster_mobile'),
        ('Promotion', '0002_remove_share_total_reward_max'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='share',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='share',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='share',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='sharerecord',
            options={'verbose_name': '\u5206\u4eab\u8bb0\u5f55', 'verbose_name_plural': '\u5206\u4eab\u8bb0\u5f55'},
        ),
        migrations.RenameField(
            model_name='sharerecord',
            old_name='created_at',
            new_name='share_time',
        ),
        migrations.AddField(
            model_name='sharerecord',
            name='activity',
            field=models.ForeignKey(related_name='share_records', default=0, to='Activity.Activity'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sharerecord',
            name='sharer',
            field=models.ForeignKey(related_name='+', default=0, verbose_name=b'\xe8\xa2\xab\xe5\x88\x86\xe4\xba\xab\xe8\x80\x85', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sharerecord',
            name='user',
            field=models.ForeignKey(related_name='+', default=1, verbose_name=b'\xe5\x88\x86\xe4\xba\xab\xe7\x9d\x80', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='sharerecord',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='sharerecord',
            name='actual_reward_for_finish',
        ),
        migrations.RemoveField(
            model_name='sharerecord',
            name='actual_reward_for_share',
        ),
        migrations.RemoveField(
            model_name='sharerecord',
            name='application',
        ),
        migrations.RemoveField(
            model_name='sharerecord',
            name='finished',
        ),
        migrations.RemoveField(
            model_name='sharerecord',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='sharerecord',
            name='share',
        ),
        migrations.RemoveField(
            model_name='sharerecord',
            name='target_user',
        ),
        migrations.DeleteModel(
            name='Share',
        ),
    ]
