# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_auto_20150922_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission',
            name='status',
            field=models.CharField(default=0, max_length=1, choices=[(0, b'Not opened'), (1, b'Opened'), (2, b'Closed'), (3, b'Finalized')]),
        ),
        migrations.AlterField(
            model_name='char',
            name='host',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='neurorequest',
            name='closed_date',
            field=models.DateField(default=datetime.datetime(2015, 9, 23, 8, 41, 23, 714928, tzinfo=utc)),
        ),
    ]
