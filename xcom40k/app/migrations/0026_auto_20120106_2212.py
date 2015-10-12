# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_auto_20150923_0843'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=10000)),
                ('pub_date', models.DateField()),
                ('author', models.ForeignKey(to='app.Account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BlogEntryTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='mission',
            name='finalize_date',
            field=models.DateField(default=datetime.datetime(2012, 1, 6, 22, 12, 50, 101184, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='neurorequest',
            name='closed_date',
            field=models.DateField(),
        ),
        migrations.AddField(
            model_name='blogentry',
            name='tags',
            field=models.ManyToManyField(to='app.BlogEntryTag'),
        ),
    ]
