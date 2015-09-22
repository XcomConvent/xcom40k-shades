# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20150922_0016'),
    ]

    operations = [
        migrations.CreateModel(
            name='NeuroRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pub_date', models.DateField()),
                ('status', models.PositiveIntegerField(default=0, choices=[(0, b'Open'), (1, b'Closed')])),
                ('closed_date', models.DateField(default=datetime.datetime(2015, 9, 22, 14, 59, 53, 898159, tzinfo=utc))),
                ('pupil', models.ForeignKey(related_name='app_neurorequest_pupil', to='app.Char')),
                ('teacher', models.ForeignKey(related_name='app_neurorequest_teacher', to='app.Char')),
            ],
        ),
    ]
