# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_neurorequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='neurorequest',
            name='target_class',
            field=models.ForeignKey(default=0, to='app.Class'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='neurorequest',
            name='closed_date',
            field=models.DateField(default=datetime.datetime(2015, 9, 22, 15, 8, 45, 609870, tzinfo=utc)),
        ),
    ]
