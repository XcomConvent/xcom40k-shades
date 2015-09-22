# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_auto_20150922_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='char',
            name='classes',
            field=models.ForeignKey(default=1, to='app.ClassLevelPair'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='neurorequest',
            name='closed_date',
            field=models.DateField(default=datetime.datetime(2015, 9, 22, 17, 53, 50, 122844, tzinfo=utc)),
        ),
    ]
