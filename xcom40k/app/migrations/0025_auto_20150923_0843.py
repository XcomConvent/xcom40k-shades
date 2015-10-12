# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_auto_20150923_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='status',
            field=models.PositiveIntegerField(default=0, choices=[(0, b'Not opened'), (1, b'Opened'), (2, b'Closed'), (3, b'Finalized')]),
        ),
        migrations.AlterField(
            model_name='neurorequest',
            name='closed_date',
            field=models.DateField(default=datetime.datetime(2015, 9, 23, 8, 43, 15, 717231, tzinfo=utc)),
        ),
    ]
