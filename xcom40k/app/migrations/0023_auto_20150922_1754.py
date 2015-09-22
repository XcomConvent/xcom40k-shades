# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_auto_20150922_1753'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='char',
            name='classes',
        ),
        migrations.AddField(
            model_name='char',
            name='classes',
            field=models.ManyToManyField(to='app.ClassLevelPair'),
        ),
        migrations.AlterField(
            model_name='neurorequest',
            name='closed_date',
            field=models.DateField(default=datetime.datetime(2015, 9, 22, 17, 54, 34, 397138, tzinfo=utc)),
        ),
    ]
