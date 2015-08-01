# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import Questionnaire.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Activity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerSheet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': '\u7b54\u5377',
                'verbose_name_plural': '\u7b54\u5377',
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=50)),
                ('multi_choice', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe4\xb8\xba\xe5\xa4\x9a\xe9\x80\x89')),
                ('order_in_list', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['order_in_list'],
                'verbose_name': '\u9009\u9879',
                'verbose_name_plural': '\u9009\u9879',
            },
        ),
        migrations.CreateModel(
            name='ChoiceQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=200, verbose_name=b'\xe9\x97\xae\xe9\xa2\x98')),
                ('required', models.BooleanField(default=True, help_text=b'\xe8\xbf\x99\xe4\xb8\xaa\xe9\x97\xae\xe9\xa2\x98\xe6\x98\xaf\xe5\x90\xa6\xe5\xbf\x85\xe9\xa1\xbb\xe5\x9b\x9e\xe7\xad\x94')),
                ('order_in_list', models.IntegerField(default=1)),
                ('multi_choice', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe4\xb8\xba\xe5\xa4\x9a\xe9\x80\x89')),
            ],
            options={
                'verbose_name': '\u9009\u62e9\u9898',
                'verbose_name_plural': '\u9009\u62e9\u9898',
            },
        ),
        migrations.CreateModel(
            name='FileAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.ImageField(upload_to=Questionnaire.models.get_file_name_from_date)),
                ('is_image', models.BooleanField(default=True)),
                ('answer_sheet', models.ForeignKey(to='Questionnaire.AnswerSheet')),
            ],
            options={
                'verbose_name': '\u6587\u4ef6\u9898',
                'verbose_name_plural': '\u6587\u4ef6\u9898',
            },
        ),
        migrations.CreateModel(
            name='MultiChoiceAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer_sheet', models.ForeignKey(to='Questionnaire.AnswerSheet')),
                ('choices', models.ManyToManyField(related_name='multi_choice_answers', to='Questionnaire.Choice')),
                ('question', models.ForeignKey(related_name='multi_choice_answers', to='Questionnaire.ChoiceQuestion')),
            ],
            options={
                'verbose_name': '\u591a\u9009\u9898',
                'verbose_name_plural': '\u591a\u9009\u9898',
            },
        ),
        migrations.CreateModel(
            name='NonChoiceQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=200, verbose_name=b'\xe9\x97\xae\xe9\xa2\x98')),
                ('required', models.BooleanField(default=True, help_text=b'\xe8\xbf\x99\xe4\xb8\xaa\xe9\x97\xae\xe9\xa2\x98\xe6\x98\xaf\xe5\x90\xa6\xe5\xbf\x85\xe9\xa1\xbb\xe5\x9b\x9e\xe7\xad\x94')),
                ('order_in_list', models.IntegerField(default=1)),
                ('type', models.SmallIntegerField(default=0, verbose_name=b'\xe4\xb8\xbb\xe8\xa7\x82\xe9\xa2\x98\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(0, b'\xe9\x97\xae\xe7\xad\x94\xe9\xa2\x98'), (1, b'\xe6\x96\x87\xe4\xbb\xb6\xe9\xa2\x98')])),
            ],
            options={
                'verbose_name': '\u4e3b\u89c2\u9898',
                'verbose_name_plural': '\u4e3b\u89c2\u9898',
            },
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('activity', models.ForeignKey(to='Activity.Activity')),
                ('participants', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'verbose_name': '\u95ee\u5377',
                'verbose_name_plural': '\u95ee\u5377',
            },
        ),
        migrations.CreateModel(
            name='SingleChoiceAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer_sheet', models.ForeignKey(to='Questionnaire.AnswerSheet')),
                ('choice', models.ForeignKey(related_name='single_choice_answers', to='Questionnaire.Choice')),
                ('question', models.ForeignKey(related_name='single_choice_answer_set', to='Questionnaire.ChoiceQuestion')),
            ],
            options={
                'verbose_name': '\u5355\u9009\u9898',
                'verbose_name_plural': '\u5355\u9009\u9898',
            },
        ),
        migrations.CreateModel(
            name='TextAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('answer_sheet', models.ForeignKey(to='Questionnaire.AnswerSheet')),
                ('question', models.ForeignKey(to='Questionnaire.NonChoiceQuestion')),
            ],
            options={
                'verbose_name': '\u7b80\u7b54\u9898',
                'verbose_name_plural': '\u7b80\u7b54\u9898',
            },
        ),
        migrations.AddField(
            model_name='nonchoicequestion',
            name='questionnaire',
            field=models.ForeignKey(to='Questionnaire.Questionnaire'),
        ),
        migrations.AddField(
            model_name='fileanswer',
            name='question',
            field=models.ForeignKey(to='Questionnaire.NonChoiceQuestion'),
        ),
        migrations.AddField(
            model_name='choicequestion',
            name='questionnaire',
            field=models.ForeignKey(to='Questionnaire.Questionnaire'),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(related_name='choices', to='Questionnaire.ChoiceQuestion'),
        ),
        migrations.AddField(
            model_name='answersheet',
            name='questionnaire',
            field=models.ForeignKey(to='Questionnaire.Questionnaire'),
        ),
        migrations.AddField(
            model_name='answersheet',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
